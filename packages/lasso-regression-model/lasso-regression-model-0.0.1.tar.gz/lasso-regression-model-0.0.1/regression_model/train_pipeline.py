import numpy as np
from config.core import config
from pipeline import price_pipe
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split


def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.app_config.training_data_file)

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[config.model_config.features],  # predictors
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.model_config.random_state,
    )
    y_train = np.log(y_train)

    # print(f"X_train: {X_train.shape}, y_train: {y_train.shape}")
    # print(f"Type X_train: {type(X_train)}")
    # print(f"Type y_train: {type(y_train)}")
    # print(f"Length of X_train: {len(X_train)}")
    # print(f"Length of y_train: {len(y_train)}")
    # print("X_train: ")
    # print("-" * 20)
    # print(X_train)
    # print("y_train: ")
    # print("-" * 20)
    # print(y_train)
    # fit model
    price_pipe.fit(X_train, y_train)
    # # ---Change
    # price_pipe = price_pipe[:-1].transform(X_train) #Exclude the last step (Lasso)
    # persist trained model
    save_pipeline(pipeline_to_persist=price_pipe)


if __name__ == "__main__":
    run_training()
