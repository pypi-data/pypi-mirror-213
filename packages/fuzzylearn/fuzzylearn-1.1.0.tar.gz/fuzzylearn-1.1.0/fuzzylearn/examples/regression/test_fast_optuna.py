import optuna
import pandas as pd
import xgboost
from category_encoders import OrdinalEncoder
from feature_engine.imputation import CategoricalImputer, MeanMedianImputer
from feature_engine.selection import DropConstantFeatures
from optuna.pruners import HyperbandPruner
from optuna.samplers import TPESampler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from zoish.feature_selectors.shap_selectors import ShapFeatureSelector

from fuzzylearn.regression.fast.fast import FLfastRegressor

urldata = "https://archive.ics.uci.edu/ml/machine-learning-databases/cpu-performance/machine.data"
# column names
col_names = [
    "vendor name",
    "Model Name",
    "MYCT",
    "MMIN",
    "MMAX",
    "CACH",
    "CHMIN",
    "CHMAX",
    "PRP",
]
# read data
data = pd.read_csv(urldata, header=None, names=col_names, sep=",")

X = data.loc[:, data.columns != "PRP"]
y = data.loc[:, data.columns == "PRP"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42
)

shap_feature_selector_factory = (
    ShapFeatureSelector.shap_feature_selector_factory.set_model_params(
        X=X_train,
        y=y_train,
        verbose=10,
        random_state=0,
        estimator=xgboost.XGBRegressor(),
        estimator_params={
            "max_depth": [4, 5],
        },
        fit_params={
            "callbacks": None,
        },
        method="optuna",
        # if n_features=None only the threshold will be considered as a cut-off of features grades.
        # if threshold=None only n_features will be considered to select the top n features.
        # if both of them are set to some values, the threshold has the priority for selecting features.
        n_features=5,
        threshold=None,
        list_of_obligatory_features_that_must_be_in_model=[],
        list_of_features_to_drop_before_any_selection=[],
    )
    .set_shap_params(
        model_output="raw",
        feature_perturbation="interventional",
        algorithm="v2",
        shap_n_jobs=-1,
        memory_tolerance=-1,
        feature_names=None,
        approximate=False,
        shortcut=False,
    )
    .set_optuna_params(
        measure_of_accuracy="r2_score(y_true, y_pred)",
        # optuna params
        with_stratified=False,
        test_size=0.3,
        n_jobs=-1,
        # optuna params
        # optuna study init params
        study=optuna.create_study(
            storage=None,
            sampler=TPESampler(),
            pruner=HyperbandPruner(),
            study_name="example of optuna optimizer",
            direction="maximize",
            load_if_exists=False,
            directions=None,
        ),
        # optuna optimization params
        study_optimize_objective=None,
        study_optimize_objective_n_trials=20,
        study_optimize_objective_timeout=600,
        study_optimize_n_jobs=-1,
        study_optimize_catch=(),
        study_optimize_callbacks=None,
        study_optimize_gc_after_trial=False,
        study_optimize_show_progress_bar=False,
    )
)

int_cols = X_train.select_dtypes(include=["int"]).columns.tolist()
float_cols = X_train.select_dtypes(include=["float"]).columns.tolist()
cat_cols = X_train.select_dtypes(include=["object"]).columns.tolist()

pipeline = Pipeline(
    [
        # int missing values imputers
        (
            "intimputer",
            MeanMedianImputer(imputation_method="median", variables=int_cols),
        ),
        # category missing values imputers
        ("catimputer", CategoricalImputer(variables=cat_cols)),
        #
        ("catencoder", OrdinalEncoder()),
        # feature selection
        ("sfsf", shap_feature_selector_factory),
    ]
)


X_train = pipeline.fit_transform(X_train, y_train)
X_test = pipeline.transform(X_test)

print("X_train.T.head()")
print(X_train.head(30))


def objective(trial):
    threshold = trial.suggest_float("threshold", 0.001, 3)
    number_of_intervals = trial.suggest_int("number_of_intervals", 5, 8)
    metric = trial.suggest_categorical("metric", ["manhattan", "euclidean"])
    model = FLfastRegressor(
        number_of_intervals=number_of_intervals, threshold=threshold, metric=metric
    ).fit(X=X_train, y=y_train, X_valid=None, y_valid=None)
    y_pred_train = model.predict(X=X_train)
    r2 = r2_score(y_train, y_pred_train)
    return r2


study = optuna.create_study(
    direction="maximize", pruner=optuna.pruners.MedianPruner(), sampler=TPESampler()
)
study.optimize(objective, n_trials=10000)
trial = study.best_trial
print("Best Score: ", trial.value)
print("Best Params: ")
for key, value in trial.params.items():
    print("  {}: {}".format(key, value))


model = FLfastRegressor(
    number_of_intervals=trial.params["number_of_intervals"],
    threshold=trial.params["threshold"],
    metric=trial.params["metric"],
).fit(X=X_train, y=y_train, X_valid=None, y_valid=None)
y_pred = model.predict(X=X_test)


print(y_pred)
print(y_test)

print("r2_score(y_test, y_pred)")
print(r2_score(y_test, y_pred))
print("mean_absolute_error(y_test, y_pred)")
print(mean_absolute_error(y_test, y_pred))
