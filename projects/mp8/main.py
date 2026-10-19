'''
Important!
Enter your full name (as it appears on Canvas) and NetID.  
If you are working in a group (maximum of 3 members), include the full names and NetIDs of all your partners.  
If you're working alone, enter `None` for the partner fields.
'''

'''
Project: MP8
Student 1: Singer Xing, mxing7
Student 2: <Name>, <NETID>
Student 3: <Name>, <NETID>
'''

# Add imports used throughout the project here
import pandas as pd
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier


class UserPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=150,
            max_depth=12,
            random_state=1,
            class_weight="balanced"
        )
        self.feature_cols = None

    def add_logs_as_features(self, users, logs):
        users = users.copy()
        logs = logs.copy()

        # make sure user_id exists
        if "user_id" not in users.columns:
            return users

        # if logs is empty, add default columns
        if logs is None or len(logs) == 0:
            users["num_visits"] = 0
            users["total_seconds"] = 0
            users["avg_seconds"] = 0
            users["max_seconds"] = 0
            users["laptop_visits"] = 0
            users["laptop_seconds"] = 0
            return users

        # basic log stats per user
        log_stats = logs.groupby("user_id").agg(
            num_visits=("url", "count"),
            total_seconds=("seconds", "sum"),
            avg_seconds=("seconds", "mean"),
            max_seconds=("seconds", "max")
        ).reset_index()

        users = users.merge(log_stats, on="user_id", how="left")

        # laptop-specific features
        laptop_logs = logs[logs["url"].astype(str).str.contains("laptop", case=False, na=False)]

        if len(laptop_logs) > 0:
            laptop_stats = laptop_logs.groupby("user_id").agg(
                laptop_visits=("url", "count"),
                laptop_seconds=("seconds", "sum")
            ).reset_index()

            users = users.merge(laptop_stats, on="user_id", how="left")
        else:
            users["laptop_visits"] = 0
            users["laptop_seconds"] = 0

        # users with no logs get NaN, replace with 0
        users = users.fillna(0)

        return users

    def prepare_features(self, users, logs):
        users = self.add_logs_as_features(users, logs)

        # convert badge into numeric dummy columns
        users = pd.get_dummies(users, columns=["badge"], drop_first=False)

        # remove columns that should not be model features
        drop_cols = ["user_id", "names"]

        for col in drop_cols:
            if col in users.columns:
                users = users.drop(columns=[col])

        return users

    def fit(self, train_users, train_logs, train_y):
        X = self.prepare_features(train_users, train_logs)

        # align y with user_id
        y = train_y.sort_values("user_id")["y"].values

        # save feature columns so predict has same columns
        self.feature_cols = X.columns

        self.model.fit(X, y)

    def predict(self, test_users, test_logs):
        X = self.prepare_features(test_users, test_logs)

        # make test columns match training columns
        X = X.reindex(columns=self.feature_cols, fill_value=0)

        preds = self.model.predict(X)

        return preds