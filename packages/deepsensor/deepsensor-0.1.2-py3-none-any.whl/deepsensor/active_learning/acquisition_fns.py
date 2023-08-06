class GreedySensorSearch:
    """
    Parent class for a greedy search algorithm that proposes locations for
    new sensor measurements from a starting set of query locations.
    """

    def __init__(
        self,
        tasks,
        N_new_sensors,
        region,
        data_processor_ID,
        reference_grid=None,
        mask_da=None,
        context_set_idx=None,
        target_var=None,
        maxormin="max",
        progressbar=0,
    ):
        """
        Args:
            tasks (dict): Dictionary mapping from dates of observation to
                tasks output by child of `ToySensorData`.
                For each task:
                    - The `X_target` entry is treated as the initial search space
                        (assumed the same for each task).
                    - The `X_context`, `Y_context` entries comprise the context set
                        (starting sensor network).

            N_new_sensors (int): The total number of new sensor locations to propose.

            reference_grid (xr.DataArray):
                If running search on a grid, contains the grid coordinates
                to search over. Used for instantiating an xr.DataArray storing acquisition
                function values.

            mask_da (boolean xr.DataArray):
                If running search on a grid, contains the grid coordinates to remove from the
                search (example use case: masking out the ocean for land sensors). Boolean True
                values are interpreted as valid points, and False as invalid points. The mask will
                be interpolated onto the search grid using nearest-neighbour interpolation
                (i.e. the mask and search grid do not need to be the same).

            maxormin (str): 'max' or 'min' - whether to maximise or minimise the
                acquisition function within each greedy search iteration.

            progressbar (int): Progress bar verbosity:
                -   0-2: no effect
                -   3: sensor progressbar
                -   4: date progressbar
                -   5: search progressbar
        """
        self.tasks = tasks
        self.N_new_sensors = N_new_sensors
        self.region = region
        self.data_processor_ID = data_processor_ID
        self.reference_grid = reference_grid
        self.mask_da = mask_da
        self.context_set_idx = context_set_idx
        self.maxormin = maxormin
        self.progressbar = progressbar

        # TODO use to determine target_set_idx?
        self.target_var = target_var

        self.dates = list(self.tasks.keys())

        # Don't edit by reference if running multiple classes with same `tasks` input
        self.tasks = copy.deepcopy(self.tasks)

        # Uninstrumented locations to search over: initialise as whole search space
        self.X_search_init = self.tasks[self.dates[0]]["X_search"][0].copy()
        if self.X_search_init.ndim == 3:
            self.X_search_init = self.X_search_init[0]
        self.search_size = self.X_search_init.shape[-1]
        self.check_X_search_large_enough()

    def check_X_search_large_enough(self):
        """Ensure number of sensors to place is less than the search space size."""
        if self.search_size < self.N_new_sensors:
            raise ValueError(
                f"Initial search size ({self.search_size}) is smaller "
                f"than number of sensors to place ({self.N_new_sensors})."
            )
        elif self.search_size == self.N_new_sensors:
            raise ValueError(
                f"Initial search size ({self.search_size}) is equal to "
                f"the number of sensors to place ({self.N_new_sensors})."
            )
        else:
            print(
                f"Placing {self.N_new_sensors} sensors in search space of {self.search_size}.\n"
            )

    def acquisition_fn(self, task, x_query, sample_i):
        """
        Acquisition function for assigning an importance value to a single
        sensor location `x_query`. To be overridden by child classes implementing
        specific acquisition functions for the greedy search.

        Child class overridden methods should take the form:
            ```
            task = self.append_query_obs_to_task(task, x_query, sample_i)
            task = self.sample_task(task, sample_i)
            # Code to compute importance of `x_query...
            return importance
            ```
        """
        raise NotImplementedError()

    def search(self, X_search):
        """
        Run one greedy pass by looping over each point in `X_search` and
        computing the acquisition function.

        If the search algorithm can be run over all points in parallel,
        this method should be overridden by the child class so that `self.run()`
        uses the parallel implementation.

        TODO check if below is still valid in GreedyOptimal:
        If the search method uses the y-values at search points (i.e. for
        an optimal benchmark), its `acquisition_fn` should expect a y_query input.
        """
        importances_list = []
        for date, task in tqdm(
            self.tasks.items(),
            desc="Date",
            position=4,
            leave=True,
            disable=self.progressbar < 4,
        ):
            for sample_i in range(self.n_samples_or_1):
                # Add size-1 dim after row dim to preserve row dim for passing to
                #   acquisition_fn. Also roll final axis to first axis for looping over search points.
                importances = []
                for x_query in tqdm(
                    np.rollaxis(X_search[:, np.newaxis], 2),
                    desc="Search",
                    position=6,
                    leave=True,
                    disable=self.progressbar < 5,
                ):
                    importance = self.acquisition_fn(task, x_query, sample_i)
                    importances.append(importance)

                importances = np.array(importances)
                self.store_acquisition_fn_values(
                    self.iteration, date, sample_i, importances
                )
                importances_list.append(importances)

        return np.mean(importances_list, axis=0)

    def select_best(self, importances, X_search):
        """Select sensor location corresponding to best importance value.

        Appends the chosen search index to a list of chosen search indexes.
        """
        if self.maxormin == "max":
            best_idx = np.argmax(importances)
        elif self.maxormin == "min":
            best_idx = np.argmin(importances)

        best_x_query = X_search[:, best_idx : best_idx + 1]

        # Index into original search space of chosen sensor location
        self.best_idxs_all.append(
            np.where((self.X_search_init == best_x_query).all(axis=0))[0][0]
        )

        return best_x_query

    def single_greedy_iteration(self):
        """
        Run a single greedy grid search iteration and append the optimal
        sensor location to self.X_new.
        """
        importances = self.search(self.X_search)
        best_x_query = self.select_best(importances, self.X_search)

        # Remove greedily chosen sensor from search space
        # TEMP turning off this so that results always on grid for storing in xarray
        #   This means 'waste' predictions over previously placed sensors/risk placing
        #   multiple sensors at same location!
        # self.X_search = self.X_search[~(self.X_search == best_x_query).all(axis=1)]

        self.X_new.append(best_x_query)
        self.iteration += 1

    def run(self):
        """
        Iteratively... docstring TODO

        Returns a tensor of proposed new sensor locations (in greedy iteration/priority order)
            and their corresponding list of indexes in the search space.
        """
        # Have separate `self.X_search` in case search space changes as placements are made
        #   (although this functionality isn't implemented yet)
        self.X_search = self.X_search_init
        self.iteration = 0

        # List of new proposed sensor locations
        self.X_new = []

        # List to track indexes into original search grid of chosen sensor locations
        #   as optimisation progresses. Used for filling y-values at chosen
        #   sensor locations, `self.X_new`
        self.best_idxs_all = []

        for _ in tqdm(
            range(self.N_new_sensors),
            desc="Placement",
            position=2,
            leave=True,
            disable=self.progressbar < 3,
        ):
            self.single_greedy_iteration()

        X_new = np.concatenate(self.X_new, axis=1)
        return X_new, self.best_idxs_all
