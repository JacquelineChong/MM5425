#!/usr/bin/env python3
"""
Build script that generates two standalone HTML files:
  1. repository.html — searchable, filterable, collapsible code repository
  2. review.html     — compact one-page review sheet (no code)

Run:  python3 build.py
"""
import html as H

def esc(s):
    return H.escape(s)

# ── Category index for ordering ──
CAT_ORDER = [
    "Data Import & File I/O",
    "Data Cleaning & Preprocessing",
    "Data Selection & Filtering",
    "Aggregation & Grouping",
    "Merging & Joining",
    "Reshaping & Pivoting",
    "Visualization",
    "Statistical Analysis & Regression",
    "String & Text Operations",
    "Other",
]

# ══════════════════════════════════════════════════════════════
#  DATA — every entry extracted from the 10 course files
# ══════════════════════════════════════════════════════════════

entries = [
# ── Data Import & File I/O ──
{"task":"Load a CSV file into a DataFrame","cat":"Data Import & File I/O",
 "fn":"pd.read_csv()","code":"import pandas as pd\ndf = pd.read_csv('filename.csv')",
 "gotcha":"For Excel use pd.read_excel(). Windows paths need r\"...\".","cmp":"read_csv for .csv, read_excel for .xlsx"},
{"task":"Load an Excel file into a DataFrame","cat":"Data Import & File I/O",
 "fn":"pd.read_excel()","code":"df = pd.read_excel('filename.xlsx')",
 "gotcha":"Requires openpyxl. Default reads first sheet.","cmp":""},
{"task":"View the first N rows of a DataFrame","cat":"Data Import & File I/O",
 "fn":"df.head()","code":"df.head()\ndf.head(3)",
 "gotcha":"Returns a view, does not modify the DataFrame.","cmp":"head() top rows; tail() bottom rows."},
{"task":"View the last N rows of a DataFrame","cat":"Data Import & File I/O",
 "fn":"df.tail()","code":"df.tail(3)",
 "gotcha":"","cmp":""},
{"task":"Check DataFrame shape (rows and columns count)","cat":"Data Import & File I/O",
 "fn":"df.shape","code":"df.shape",
 "gotcha":"shape is an attribute, not a method — no parentheses.","cmp":""},
{"task":"Inspect column data types and non-null counts","cat":"Data Import & File I/O",
 "fn":"df.info()","code":"df.info()",
 "gotcha":"Prints to console, returns None. Useful for spotting missing values and wrong dtypes.","cmp":"info() types+nulls; describe() numeric stats."},
{"task":"Get summary statistics for numeric columns","cat":"Data Import & File I/O",
 "fn":"df.describe()","code":"df.describe()",
 "gotcha":"Only numeric by default. For object columns: df[['col']].describe().","cmp":""},
{"task":"List all column names in a DataFrame","cat":"Data Import & File I/O",
 "fn":"df.columns","code":"df.columns",
 "gotcha":"Returns an Index object. list(df.columns) for a plain list.","cmp":""},

# ── Data Cleaning & Preprocessing ──
{"task":"Fill missing numeric values with the column mean","cat":"Data Cleaning & Preprocessing",
 "fn":"fillna(), .mean()","code":"df['Income'].fillna(df['Income'].mean(), inplace=True)",
 "gotcha":"inplace=True modifies original. Without it returns new DataFrame.","cmp":"fillna replaces NaN; dropna removes rows."},
{"task":"Fill missing values with a constant (zero or string)","cat":"Data Cleaning & Preprocessing",
 "fn":"fillna()","code":"df['Experience'].fillna(0, inplace=True)\ndf['County'].fillna('Unknown', inplace=True)",
 "gotcha":"Choose a fill value that makes domain sense.","cmp":""},
{"task":"Fill missing values using another column as fallback","cat":"Data Cleaning & Preprocessing",
 "fn":"np.where(), .isna()","code":"import numpy as np\ndf['discounted_price'] = np.where(\n    df['discounted_price'].isna(),\n    df['original_price'],\n    df['discounted_price'])",
 "gotcha":"np.where(condition, if_true, if_false) is element-wise.","cmp":""},
{"task":"Drop rows where a specific column has missing values","cat":"Data Cleaning & Preprocessing",
 "fn":"df.dropna()","code":"df = df.dropna(subset=['score']).copy()",
 "gotcha":"subset= specifies columns. .copy() avoids SettingWithCopyWarning.","cmp":"dropna removes; fillna replaces."},
{"task":"Drop a column from a DataFrame","cat":"Data Cleaning & Preprocessing",
 "fn":"df.drop()","code":"df = df.drop('ID', axis=1)\ndf = df.drop(columns='cogs')",
 "gotcha":"axis=1 means columns, axis=0 means rows.","cmp":""},
{"task":"Count missing values per column","cat":"Data Cleaning & Preprocessing",
 "fn":"isnull().sum()","code":"df.isnull().sum()",
 "gotcha":"isnull() and isna() are identical in pandas.","cmp":""},
{"task":"Create dummy variables (one-hot encoding) for a categorical column","cat":"Data Cleaning & Preprocessing",
 "fn":"pd.get_dummies(), pd.concat()","code":"credit = pd.get_dummies(df['CreditCard'], prefix='credit')\ndf = pd.concat([df, credit], axis=1)\ndf.drop('CreditCard', axis=1, inplace=True)",
 "gotcha":"drop_first=True avoids multicollinearity. dtype=int for 0/1.","cmp":"get_dummies is pandas; OneHotEncoder is sklearn."},
{"task":"One-hot encode multiple categorical columns at once","cat":"Data Cleaning & Preprocessing",
 "fn":"pd.get_dummies()","code":"movie = pd.get_dummies(movie,\n    columns=['genre','country'], dtype=int)",
 "gotcha":"Passing columns= encodes all at once. Original columns auto-dropped.","cmp":""},
{"task":"Map categorical string values to numeric codes","cat":"Data Cleaning & Preprocessing",
 "fn":".map()","code":"df['CreditCard'] = df['CreditCard'].map({'Yes':1, 'No':0})",
 "gotcha":"Values not in the mapping dictionary become NaN.","cmp":"map() on Series; replace() on DataFrame."},
{"task":"Clip values to a valid range","cat":"Data Cleaning & Preprocessing",
 "fn":".clip()","code":"df['popularity'] = df['popularity'].clip(0, 100)",
 "gotcha":"clip(lower, upper) caps values at both ends.","cmp":""},
{"task":"Replace out-of-range values with the column mean","cat":"Data Cleaning & Preprocessing",
 "fn":".loc[], .mean()","code":"df.loc[(df['Age']<13)|(df['Age']>100), 'Age'] = df['Age'].mean()",
 "gotcha":"Mean is computed before replacement, so outliers affect it.","cmp":""},
{"task":"Cap percentage columns to 0-100 range","cat":"Data Cleaning & Preprocessing",
 "fn":".loc[]","code":"for c in percent_cols:\n    df.loc[df[c]<0, c] = 0\n    df.loc[df[c]>100, c] = 100",
 "gotcha":"Always validate rate/percentage columns in real data.","cmp":""},
{"task":"Convert a column to numeric type, coercing errors to NaN","cat":"Data Cleaning & Preprocessing",
 "fn":"pd.to_numeric()","code":"df['price'] = pd.to_numeric(df['price'], errors='coerce')",
 "gotcha":"errors='coerce' turns unparseable strings into NaN.","cmp":""},
{"task":"Convert a column to datetime and extract date parts","cat":"Data Cleaning & Preprocessing",
 "fn":"pd.to_datetime(), .dt accessor","code":"df['dt'] = pd.to_datetime(df['date'], errors='coerce')\ndf['month'] = df['dt'].dt.month\ndf['weekday'] = df['dt'].dt.weekday",
 "gotcha":"dt.weekday: Monday=0 through Sunday=6. Bad dates become NaT.","cmp":""},
{"task":"Compute the number of days between two date columns","cat":"Data Cleaning & Preprocessing",
 "fn":"datetime subtraction, .dt.days","code":"df['days'] = (df['end_dt'] - df['start_dt']).dt.days",
 "gotcha":"Result is timedelta; use .dt.days for integer. NaT produces NaN.","cmp":""},
{"task":"Parse a time string and extract the hour","cat":"Data Cleaning & Preprocessing",
 "fn":"pd.to_datetime(), .dt.hour","code":"t = pd.to_datetime(df['Time'], format='%H:%M')\ndf['Hour'] = t.dt.hour",
 "gotcha":"Specify format= to match your time string pattern.","cmp":""},
{"task":"Convert a boolean column to integer 0/1","cat":"Data Cleaning & Preprocessing",
 "fn":".astype(int)","code":"df['explicit'] = df['explicit'].astype(int)",
 "gotcha":"True→1, False→0. NaN values will cause an error — fill first.","cmp":""},
{"task":"Convert milliseconds to minutes","cat":"Data Cleaning & Preprocessing",
 "fn":"arithmetic","code":"df['duration_min'] = df['duration_ms'] / 60000",
 "gotcha":"","cmp":""},
{"task":"Standardize (z-score normalize) numeric features","cat":"Data Cleaning & Preprocessing",
 "fn":"StandardScaler, fit_transform()","code":"from sklearn.preprocessing import StandardScaler\nscaler = StandardScaler()\nX_train_s = pd.DataFrame(\n    scaler.fit_transform(X_train), columns=X_train.columns)\nX_test_s = pd.DataFrame(\n    scaler.transform(X_test), columns=X_test.columns)",
 "gotcha":"Always fit on training data only, then transform both train and test. fit_transform on test leaks info.","cmp":"fit_transform = fit+transform. transform alone on test."},
{"task":"Apply log transformation to skewed numeric columns","cat":"Data Cleaning & Preprocessing",
 "fn":"np.log1p()","code":"df['col_log'] = np.log1p(df['col'])",
 "gotcha":"log1p(x)=log(1+x), safe when x=0. Cannot handle negatives — clip first.","cmp":""},
{"task":"Create a binary flag column using a condition","cat":"Data Cleaning & Preprocessing",
 "fn":"np.where()","code":"df['Prefer'] = np.where(df['score']>=6.5, 1, 0)",
 "gotcha":"np.where returns an array. Assigning to a column works fine.","cmp":""},
{"task":"Create polynomial / interaction features","cat":"Data Cleaning & Preprocessing",
 "fn":"arithmetic","code":"df['runtime_sq'] = df['runtime'] ** 2\ndf['spend'] = df['purchases'] * df['avg_order']",
 "gotcha":"Too many interaction terms can cause overfitting.","cmp":""},
{"task":"Create ratio features with safe division","cat":"Data Cleaning & Preprocessing",
 "fn":"arithmetic","code":"df['rate'] = df['count'] / (df['years'] + 1e-6)",
 "gotcha":"Adding a small constant to the denominator prevents division by zero.","cmp":""},
{"task":"Identify categorical vs numeric columns automatically","cat":"Data Cleaning & Preprocessing",
 "fn":"select_dtypes()","code":"cat_cols = df.select_dtypes(include=['object']).columns.tolist()\nnum_cols = df.select_dtypes(include=['number']).columns.tolist()",
 "gotcha":"'object' catches strings. Boolean columns may need include=['bool'].","cmp":""},
{"task":"Fill all missing numeric values with column means at once","cat":"Data Cleaning & Preprocessing",
 "fn":"fillna(), .mean()","code":"df = df.fillna(df.mean(numeric_only=True))",
 "gotcha":"numeric_only=True skips non-numeric columns.","cmp":""},
{"task":"Fill remaining NaN values with column median","cat":"Data Cleaning & Preprocessing",
 "fn":"fillna(), .median()","code":"X = X.fillna(X.median(numeric_only=True))",
 "gotcha":"Median is more robust to outliers than mean.","cmp":""},
{"task":"Look up US ZIP codes to get county/state names","cat":"Data Cleaning & Preprocessing",
 "fn":"pgeocode.Nominatim, query_postal_code()","code":"import pgeocode\nnomi = pgeocode.Nominatim('us')\nout = nomi.query_postal_code(df['ZIP'].astype(str).tolist())\ndf['County'] = out['county_name'].values",
 "gotcha":"Requires pip install pgeocode. ZIP codes must be strings.","cmp":""},
{"task":"Check skewness of numeric columns","cat":"Data Cleaning & Preprocessing",
 "fn":".skew()","code":"df[num_cols].skew().sort_values(ascending=False)",
 "gotcha":"Absolute skewness > 3 indicates strong skew. Consider log transform.","cmp":""},

# ── Data Selection & Filtering ──
{"task":"Select specific columns from a DataFrame by name","cat":"Data Selection & Filtering",
 "fn":"df[[col1, col2]]","code":"df[['Customer type', 'City']]",
 "gotcha":"Double brackets [[ ]] return a DataFrame; single brackets return a Series.","cmp":""},
{"task":"Select rows and columns by integer position","cat":"Data Selection & Filtering",
 "fn":"df.iloc[]","code":"df.iloc[0:2, :3]",
 "gotcha":"iloc uses exclusive end index. iloc[0:2] returns rows 0 and 1, not 2.","cmp":"iloc = integer position; loc = label name. loc[0:2] includes 2."},
{"task":"Select rows and columns by label names","cat":"Data Selection & Filtering",
 "fn":"df.loc[]","code":"df.loc[0:2, :'Customer type']",
 "gotcha":"loc end index is inclusive — loc[0:2] returns rows 0, 1, AND 2.","cmp":"loc label-based; iloc position-based."},
{"task":"Filter rows by a single condition","cat":"Data Selection & Filtering",
 "fn":"df.loc[condition]","code":"df.loc[df['Branch']=='A', 'Customer type']",
 "gotcha":"Use == for comparison, not =.","cmp":""},
{"task":"Filter rows by multiple conditions (AND / OR)","cat":"Data Selection & Filtering",
 "fn":"df.loc[], & | operators","code":"df.loc[(df['Branch']=='A') & (df['Qty']>5)]\ndf.loc[(df['Gender']=='F') | (df['Line']=='Health')]",
 "gotcha":"Each condition must be in parentheses. Use & for AND, | for OR — not Python and/or.","cmp":""},
{"task":"Create a filtered subset of a DataFrame for analysis","cat":"Data Selection & Filtering",
 "fn":"df.loc[]","code":"member_df = df.loc[df['Customer type']=='Member']\nnormal_df = df.loc[df['Customer type']=='Normal']",
 "gotcha":"The filtered DataFrame shares memory with the original. Use .copy() to modify safely.","cmp":""},
{"task":"Separate features (X) and target (y) for modeling","cat":"Data Selection & Filtering",
 "fn":"df.drop(), df.iloc[]","code":"X = df.drop('Personal.Loan', axis='columns')\ny = df['Personal.Loan']\n# or:\nX = df.iloc[:, :-1]\ny = df.iloc[:, -1]",
 "gotcha":"Make sure X does not contain the target column.","cmp":""},
{"task":"Collect column names matching a prefix pattern","cat":"Data Selection & Filtering",
 "fn":"list comprehension","code":"genre_cols = [c for c in df.columns if c.startswith('genre_')]",
 "gotcha":"Case-sensitive unless you use .lower().","cmp":""},
{"task":"Remove cancellations and invalid rows from retail data","cat":"Data Selection & Filtering",
 "fn":"boolean indexing, .str methods","code":"df = df[df['Quantity'] > 0]\ndf = df[~df['InvoiceNo'].astype(str).str.startswith('C')]\ndf = df[~df['Description'].str.contains('POSTAGE', na=False)]",
 "gotcha":"~ is the NOT operator. na=False in str.contains prevents NaN errors.","cmp":""},

# ── Aggregation & Grouping ──
{"task":"Count occurrences of each unique value in a column","cat":"Aggregation & Grouping",
 "fn":"value_counts()","code":"df['City'].value_counts()",
 "gotcha":"Sorted descending. NaN excluded by default — use dropna=False to include.","cmp":"value_counts() counts; nunique() just the count of distinct values."},
{"task":"Get relative frequencies (proportions) of unique values","cat":"Aggregation & Grouping",
 "fn":"value_counts(normalize=True)","code":"df['City'].value_counts(normalize=True)",
 "gotcha":"normalize=True converts counts to proportions summing to 1.0.","cmp":""},
{"task":"Count the number of unique values in a column","cat":"Aggregation & Grouping",
 "fn":".nunique()","code":"df['Product line'].nunique()",
 "gotcha":"nunique() excludes NaN by default.","cmp":"nunique() = count; unique() = actual values."},
{"task":"List all unique values in a column","cat":"Aggregation & Grouping",
 "fn":".unique()","code":"df['Rating'].unique()",
 "gotcha":"Returns a NumPy array, not a list. Includes NaN if present.","cmp":""},
{"task":"Describe summary statistics for a subset of columns","cat":"Aggregation & Grouping",
 "fn":".describe()","code":"member_df[['Total','gross income','Quantity']].describe()",
 "gotcha":"Shows count, mean, std, min, 25%, 50%, 75%, max.","cmp":""},
{"task":"Compute aggregate statistics using .agg()","cat":"Aggregation & Grouping",
 "fn":".agg()","code":"df[['Age','Purchases']].agg(['min','max'])",
 "gotcha":"agg() accepts a list of function names or actual functions.","cmp":""},
{"task":"Group by a column and count items per group using transform","cat":"Aggregation & Grouping",
 "fn":"groupby(), .transform()","code":"df['album_songs'] = df.groupby(\n    ['artist','album'])['track_id'].transform('count')",
 "gotcha":"transform returns same-length Series for direct column assignment.","cmp":"transform broadcasts back; agg collapses groups."},
{"task":"Compute cumulative count within groups","cat":"Aggregation & Grouping",
 "fn":"groupby().cumcount()","code":"df['song_num'] = df.groupby('artist').cumcount()",
 "gotcha":"cumcount starts at 0. Data must be sorted first.","cmp":"cumcount = running position; transform('count') = total."},
{"task":"Get the minimum value within each group using transform","cat":"Aggregation & Grouping",
 "fn":"groupby().transform('min')","code":"df['first_year'] = df.groupby('artist')['year'].transform('min')",
 "gotcha":"Broadcasts the group minimum back to every row.","cmp":""},
{"task":"Compute group-level means for cluster profiling","cat":"Aggregation & Grouping",
 "fn":"groupby().mean()","code":"profile = df.groupby('cluster')[features].mean().round(2)",
 "gotcha":"mean() only works on numeric columns.","cmp":""},
{"task":"Compute value counts within filtered subsets and combine","cat":"Aggregation & Grouping",
 "fn":"value_counts(), pd.concat()","code":"sA = df.loc[df['Branch']=='A','Type'].value_counts(normalize=True)\nsB = df.loc[df['Branch']=='B','Type'].value_counts(normalize=True)\nshares = pd.concat([sA, sB], axis=1)\nshares.columns = ['A','B']",
 "gotcha":"Each value_counts returns a Series; concat axis=1 joins side by side.","cmp":""},
{"task":"Analyze genre distribution within each cluster","cat":"Aggregation & Grouping",
 "fn":"groupby, value_counts(normalize=True)","code":"for c in sorted(df['cluster'].unique()):\n    print(df.loc[df['cluster']==c,'genre']\n          .value_counts(normalize=True).head(5))",
 "gotcha":"K-means does not use genre labels, but comparing helps interpretation.","cmp":""},

# ── Merging & Joining ──
{"task":"Concatenate DataFrames vertically (stack rows)","cat":"Merging & Joining",
 "fn":"pd.concat(), axis=0","code":"pd.concat([d1, d2], ignore_index=True, axis=0)",
 "gotcha":"axis=0 stacks rows (default). ignore_index=True resets the index.","cmp":""},
{"task":"Concatenate DataFrames horizontally (side by side)","cat":"Merging & Joining",
 "fn":"pd.concat(), axis=1","code":"pd.concat([d1, d2], axis=1)",
 "gotcha":"axis=1 joins columns side by side. Rows aligned by index — mismatched indices produce NaN.","cmp":"concat aligns by index; merge by key columns."},
{"task":"Merge location data back into the main DataFrame","cat":"Merging & Joining",
 "fn":"df.merge()","code":"df = df.merge(other_df,\n    on=['artist','album'], how='left')",
 "gotcha":"Default how='inner' drops non-matching rows. Use how='left' to keep all left rows.","cmp":"merge on column values; concat on index."},

# ── Reshaping & Pivoting ──
{"task":"Pivot a long transaction table into a wide basket matrix","cat":"Reshaping & Pivoting",
 "fn":"groupby().unstack()","code":"basket = df.groupby(['InvoiceNo','Description'])['Qty']\\\n    .sum().unstack(fill_value=0)\nbasket = (basket > 0).astype(int)",
 "gotcha":"unstack moves inner index to columns. fill_value=0 replaces NaN.","cmp":"unstack inverse of stack. pivot_table alternative."},
{"task":"Transpose a DataFrame (swap rows and columns)","cat":"Reshaping & Pivoting",
 "fn":".T","code":"shares.T",
 "gotcha":".T is shorthand for .transpose(). Column names become the new index.","cmp":""},

# ── Visualization ──
{"task":"Plot histograms for all numeric columns in a DataFrame","cat":"Visualization",
 "fn":"df.hist(), plt.show()","code":"df.hist(figsize=(20,25))\nplt.show()",
 "gotcha":"hist() creates one subplot per numeric column. Adjust figsize for readability.","cmp":""},
{"task":"Plot a histogram for a single column","cat":"Visualization",
 "fn":".hist(), plt labels","code":"df['Unit price'].hist()\nplt.xlabel('Unit price')\nplt.ylabel('Frequency')\nplt.title('Price distribution')",
 "gotcha":"Default bins=10. Increase bins for finer granularity.","cmp":""},
{"task":"Plot a bar chart from value counts","cat":"Visualization",
 "fn":"value_counts().plot(kind='bar')","code":"df['Gender'].value_counts().plot(kind='bar')",
 "gotcha":"kind='bar' for vertical; kind='barh' for horizontal.","cmp":""},
{"task":"Plot a grouped bar chart comparing categories","cat":"Visualization",
 "fn":".plot(kind='bar')","code":"shares.T.plot(kind='bar')\nplt.legend(title='Customer type',\n    bbox_to_anchor=(1.01, 1), loc='upper left')\nplt.show()",
 "gotcha":"bbox_to_anchor moves the legend outside the plot area.","cmp":""},
{"task":"Create a scatter plot to visualize correlation","cat":"Visualization",
 "fn":"plt.scatter()","code":"plt.scatter(x=df['Quantity'], y=df['gross income'])\nplt.xlabel('Quantity')\nplt.ylabel('gross income')",
 "gotcha":"Scatter plots show relationships but do not prove causation.","cmp":""},
{"task":"Create a scatter plot with regression trend line and confidence band","cat":"Visualization",
 "fn":"sns.regplot()","code":"sns.regplot(data=df, x='Unit price', y='Rating')\nplt.title('regplot: Unit price vs Rating')\nplt.show()",
 "gotcha":"regplot adds a linear fit + 95% CI band by default.","cmp":""},
{"task":"Plot a heatmap of correlations among numeric columns","cat":"Visualization",
 "fn":"sns.heatmap(), .corr()","code":"sns.heatmap(final.corr(numeric_only=True),\n    annot=True, cmap='coolwarm')\nplt.show()",
 "gotcha":"corr() computes Pearson correlation (linear only). annot=True prints values.","cmp":""},
{"task":"Plot a confusion matrix","cat":"Visualization",
 "fn":"ConfusionMatrixDisplay","code":"from sklearn.metrics import ConfusionMatrixDisplay\nConfusionMatrixDisplay.from_predictions(y_test, y_pred)\nplt.show()",
 "gotcha":"from_predictions takes actual and predicted labels. from_estimator takes model + test data.","cmp":""},
{"task":"Plot an ROC curve","cat":"Visualization",
 "fn":"RocCurveDisplay","code":"from sklearn.metrics import RocCurveDisplay\nRocCurveDisplay.from_predictions(y_test, y_proba)\nplt.show()",
 "gotcha":"ROC curves need predicted probabilities, not class labels. Use predict_proba()[:,1].","cmp":""},
{"task":"Plot predicted vs actual values for regression","cat":"Visualization",
 "fn":"plt.scatter(), plt.plot()","code":"plt.scatter(y_test, y_pred)\nplt.plot([y_test.min(), y_test.max()],\n         [y_test.min(), y_test.max()], 'r--')\nplt.xlabel('Actual')\nplt.ylabel('Predicted')\nplt.show()",
 "gotcha":"Points on the diagonal = perfect predictions. Spread = error.","cmp":""},
{"task":"Plot training vs test error to visualize overfitting","cat":"Visualization",
 "fn":"plt.plot()","code":"plt.plot(curve_df['nodes'], curve_df['train_error'], label='Train')\nplt.plot(curve_df['nodes'], curve_df['test_error'], '--', label='Test')\nplt.xlabel('Number of nodes')\nplt.legend()\nplt.show()",
 "gotcha":"When train error drops but test error rises, the model is overfitting.","cmp":""},
{"task":"Plot the elbow method for K-means clustering","cat":"Visualization",
 "fn":"KMeans.inertia_, plt.plot()","code":"ssd = []\nfor k in range(1, 20):\n    km = KMeans(n_clusters=k, n_init=10, random_state=42)\n    km.fit(X_scaled)\n    ssd.append(km.inertia_)\nplt.plot(range(1,20), ssd, 'o-')\nplt.xlabel('k')\nplt.ylabel('SSD / inertia')\nplt.show()",
 "gotcha":"inertia_ is sum of squared distances to cluster centers. Look for the elbow bend.","cmp":""},
{"task":"Plot a 2D scatter plot colored by cluster assignment","cat":"Visualization",
 "fn":"sns.scatterplot(), hue=","code":"sns.scatterplot(data=df, x='danceability', y='energy',\n    hue='cluster', palette='deep')\nplt.show()",
 "gotcha":"hue= colors points by a categorical column.","cmp":""},
{"task":"Plot KNN accuracy or RMSE vs K to choose optimal K","cat":"Visualization",
 "fn":"plt.plot()","code":"plt.plot(k_values, test_acc, marker='o', label='Test accuracy')\nplt.xlabel('K')\nplt.ylabel('Accuracy')\nplt.legend()\nplt.show()",
 "gotcha":"Very small K overfits; very large K over-smooths.","cmp":""},
{"task":"Plot feature importances from a decision tree","cat":"Visualization",
 "fn":".feature_importances_, .plot(kind='bar')","code":"imp = pd.Series(best_tree.feature_importances_,\n    index=X.columns).sort_values(ascending=False)\nimp.head(20).plot(kind='bar')\nplt.ylabel('importance')\nplt.show()",
 "gotcha":"feature_importances_ sums to 1.0. Higher = more important for splitting.","cmp":""},
{"task":"Plot regression coefficients as a horizontal bar chart","cat":"Visualization",
 "fn":"pd.Series, .plot(kind='barh')","code":"coefs = pd.Series(model.coef_, index=X.columns)\ncoefs.sort_values().plot(kind='barh')\nplt.show()",
 "gotcha":"Coefficients are only comparable if features are standardized.","cmp":""},
{"task":"Create subplots to show histograms of many columns in a grid","cat":"Visualization",
 "fn":"plt.subplots(), sns.histplot()","code":"fig, axes = plt.subplots(n_rows, n_cols, figsize=(14,8))\nfor i, col in enumerate(num_cols):\n    sns.histplot(df[col], ax=axes.ravel()[i])\n    axes.ravel()[i].set_title(col)\nplt.tight_layout()\nplt.show()",
 "gotcha":"axes.ravel() flattens the 2D array for easy looping. Turn off unused subplots.","cmp":""},

# ── Statistical Analysis & Regression ──
{"task":"Split data into training and testing sets","cat":"Statistical Analysis & Regression",
 "fn":"train_test_split()","code":"from sklearn.model_selection import train_test_split\nX_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42)",
 "gotcha":"random_state ensures reproducibility. test_size=0.2 means 20% test.","cmp":""},
{"task":"Split data with stratification to preserve class proportions","cat":"Statistical Analysis & Regression",
 "fn":"train_test_split(stratify=)","code":"X_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.2, random_state=42, stratify=y)",
 "gotcha":"stratify=y ensures both sets have similar class ratios. Essential for imbalanced data.","cmp":""},
{"task":"Train a Decision Tree Classifier","cat":"Statistical Analysis & Regression",
 "fn":"DecisionTreeClassifier(), .fit()","code":"from sklearn.tree import DecisionTreeClassifier\ndt = DecisionTreeClassifier(criterion='entropy', random_state=42)\ndt.fit(X_train, y_train)",
 "gotcha":"criterion='entropy' uses information gain; 'gini' (default) uses Gini impurity.","cmp":""},
{"task":"Train a Decision Tree Classifier with pruning to reduce overfitting","cat":"Statistical Analysis & Regression",
 "fn":"DecisionTreeClassifier(max_depth=, min_samples_leaf=)","code":"dt = DecisionTreeClassifier(\n    max_depth=5, min_samples_split=20,\n    min_samples_leaf=10, random_state=42)\ndt.fit(X_train, y_train)",
 "gotcha":"Smaller max_depth and larger min_samples_leaf = simpler trees (pre-pruning).","cmp":""},
{"task":"Train a Decision Tree Regressor","cat":"Statistical Analysis & Regression",
 "fn":"DecisionTreeRegressor(), .fit()","code":"from sklearn.tree import DecisionTreeRegressor\nreg_tree = DecisionTreeRegressor(random_state=42)\nreg_tree.fit(X_train, y_train)",
 "gotcha":"Evaluate with MAE/RMSE/R2 instead of accuracy.","cmp":""},
{"task":"Visualize a decision tree using graphviz","cat":"Statistical Analysis & Regression",
 "fn":"tree.export_graphviz(), graphviz.Source()","code":"from sklearn import tree\nimport graphviz\ndot = tree.export_graphviz(dt, feature_names=X.columns,\n    class_names=['0','1'], filled=True, proportion=True)\ngraphviz.Source(dot)",
 "gotcha":"max_depth= in export_graphviz limits visualization depth, not the actual tree. class_names must be strings.","cmp":""},
{"task":"Check tree complexity (node count and depth)","cat":"Statistical Analysis & Regression",
 "fn":".tree_.node_count, .tree_.max_depth","code":"print('Nodes:', dt.tree_.node_count)\nprint('Depth:', dt.tree_.max_depth)",
 "gotcha":"Accessed via .tree_ attribute of the fitted model.","cmp":""},
{"task":"Predict class labels using a trained classifier","cat":"Statistical Analysis & Regression",
 "fn":".predict()","code":"y_pred = dt.predict(X_test)",
 "gotcha":"predict() returns class labels (0/1). For probabilities use predict_proba().","cmp":""},
{"task":"Predict class probabilities using a trained classifier","cat":"Statistical Analysis & Regression",
 "fn":".predict_proba()","code":"y_proba = dt.predict_proba(X_test)[:, 1]",
 "gotcha":"Returns a 2D array. [:,1] gets the positive class probability.","cmp":""},
{"task":"Evaluate classification with accuracy score","cat":"Statistical Analysis & Regression",
 "fn":"accuracy_score()","code":"from sklearn.metrics import accuracy_score\naccuracy_score(y_test, y_pred)",
 "gotcha":"Accuracy can be misleading with imbalanced classes.","cmp":""},
{"task":"Evaluate classification with precision, recall, F1, and AUC","cat":"Statistical Analysis & Regression",
 "fn":"precision_score(), recall_score(), f1_score(), roc_auc_score()","code":"from sklearn.metrics import (precision_score, recall_score,\n    f1_score, roc_auc_score)\nprint('Prec:', precision_score(y_test, y_pred, zero_division=0))\nprint('Rec:', recall_score(y_test, y_pred))\nprint('F1:', f1_score(y_test, y_pred))\nprint('AUC:', roc_auc_score(y_test, y_proba))",
 "gotcha":"Precision=TP/(TP+FP), Recall=TP/(TP+FN). AUC needs probabilities not labels.","cmp":""},
{"task":"Generate a full classification report","cat":"Statistical Analysis & Regression",
 "fn":"classification_report()","code":"from sklearn.metrics import classification_report\nprint(classification_report(y_test, y_pred))",
 "gotcha":"Shows precision, recall, F1 for each class plus macro/weighted averages.","cmp":""},
{"task":"Compute and display a confusion matrix as a DataFrame","cat":"Statistical Analysis & Regression",
 "fn":"confusion_matrix()","code":"from sklearn.metrics import confusion_matrix\npd.DataFrame(confusion_matrix(y_test, y_pred),\n    columns=['Pred 0','Pred 1'],\n    index=['Act 0','Act 1'])",
 "gotcha":"Rows = actual, columns = predicted. Top-left = TN, bottom-right = TP.","cmp":""},
{"task":"Evaluate regression with MAE, RMSE, and R-squared","cat":"Statistical Analysis & Regression",
 "fn":"mean_absolute_error(), mean_squared_error(), r2_score()","code":"from sklearn.metrics import (mean_absolute_error,\n    mean_squared_error, r2_score)\nprint('MAE:', mean_absolute_error(y_test, y_pred))\nprint('RMSE:', np.sqrt(mean_squared_error(y_test, y_pred)))\nprint('R2:', r2_score(y_test, y_pred))",
 "gotcha":"sklearn returns MSE not RMSE — take np.sqrt(). R2 can be negative if worse than mean.","cmp":""},
{"task":"Perform 5-fold cross-validation for classification","cat":"Statistical Analysis & Regression",
 "fn":"StratifiedKFold, cross_validate()","code":"from sklearn.model_selection import StratifiedKFold, cross_validate\ncv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)\nscores = cross_validate(dt, X, y, cv=cv,\n    scoring=['accuracy','f1','roc_auc'])",
 "gotcha":"StratifiedKFold preserves class proportions in each fold.","cmp":""},
{"task":"Perform 5-fold cross-validation for regression","cat":"Statistical Analysis & Regression",
 "fn":"KFold, cross_validate()","code":"from sklearn.model_selection import KFold, cross_validate\ncv = KFold(n_splits=5, shuffle=True, random_state=42)\nscores = cross_validate(model, X, y, cv=cv,\n    scoring=['neg_mean_absolute_error','r2'])",
 "gotcha":"sklearn uses NEGATIVE MAE/RMSE for CV scoring. Multiply by -1 to get normal values.","cmp":""},
{"task":"Get out-of-fold predictions from cross-validation","cat":"Statistical Analysis & Regression",
 "fn":"cross_val_predict()","code":"from sklearn.model_selection import cross_val_predict\noof_proba = cross_val_predict(dt, X, y, cv=cv,\n    method='predict_proba')[:, 1]",
 "gotcha":"Each sample is predicted by a model that did NOT train on it.","cmp":""},
{"task":"Tune hyperparameters using GridSearchCV","cat":"Statistical Analysis & Regression",
 "fn":"GridSearchCV()","code":"from sklearn.model_selection import GridSearchCV\nparam_grid = {'max_depth':[3,5,8],\n    'min_samples_leaf':[1,5,10]}\ngrid = GridSearchCV(dt, param_grid, cv=5,\n    scoring='roc_auc', refit='roc_auc', n_jobs=-1)\ngrid.fit(X_train, y_train)",
 "gotcha":"refit= selects metric for best model. n_jobs=-1 uses all cores. Tune on train only.","cmp":""},
{"task":"Inspect GridSearchCV results and rank parameter combinations","cat":"Statistical Analysis & Regression",
 "fn":"grid.cv_results_","code":"results = pd.DataFrame(grid.cv_results_)\nresults.sort_values('rank_test_score').head()",
 "gotcha":"cv_results_ contains mean/std scores for every parameter combination.","cmp":""},
{"task":"Train a baseline Linear Regression model","cat":"Statistical Analysis & Regression",
 "fn":"LinearRegression(), .fit()","code":"from sklearn.linear_model import LinearRegression\nlr = LinearRegression()\nlr.fit(X_train, y_train)",
 "gotcha":"Linear regression has no hyperparameters to tune (OLS). Minimizes squared error.","cmp":""},
{"task":"Interpret linear regression coefficients","cat":"Statistical Analysis & Regression",
 "fn":".coef_, pd.Series","code":"coef = pd.Series(lr.coef_, index=X.columns)\ncoef.sort_values(key=np.abs, ascending=False).head(20)",
 "gotcha":"Coefficients are only comparable if features are on the same scale. Standardize first.","cmp":""},
{"task":"Train a Logistic Regression classifier","cat":"Statistical Analysis & Regression",
 "fn":"LogisticRegression(), .fit()","code":"from sklearn.linear_model import LogisticRegression\nlg = LogisticRegression(max_iter=5000, random_state=42)\nlg.fit(X_train, y_train)",
 "gotcha":"Increase max_iter if you get a convergence warning. Outputs probabilities via predict_proba.","cmp":""},
{"task":"Train a Gaussian Naive Bayes classifier","cat":"Statistical Analysis & Regression",
 "fn":"GaussianNB(), .fit()","code":"from sklearn.naive_bayes import GaussianNB\nnb = GaussianNB()\nnb.fit(X_train, y_train)",
 "gotcha":"Assumes feature independence given the class. Sensitive to scale — standardize or log-transform.","cmp":""},
{"task":"Inspect Naive Bayes class priors","cat":"Statistical Analysis & Regression",
 "fn":".class_prior_, .classes_","code":"for c, p in zip(nb.classes_, nb.class_prior_):\n    print(f'Class {c}: {p:.4f}')",
 "gotcha":"class_prior_ reflects the training set class distribution.","cmp":""},
{"task":"Compare feature means between classes for interpretation","cat":"Statistical Analysis & Regression",
 "fn":"groupby, mean difference","code":"means = df.groupby('target')[features].mean()\ndiff = (means.loc[1] - means.loc[0]).sort_values()",
 "gotcha":"Positive difference = feature is higher for class 1.","cmp":""},
{"task":"Train a K-Means clustering model","cat":"Statistical Analysis & Regression",
 "fn":"KMeans(), .fit_predict()","code":"from sklearn.cluster import KMeans\nkm = KMeans(n_clusters=9, n_init=10, random_state=42)\nlabels = km.fit_predict(X_scaled)",
 "gotcha":"Unsupervised — no target variable. Always standardize first. n_init=10 runs 10 times.","cmp":""},
{"task":"Compute SSD decrease per K to find optimal clusters","cat":"Statistical Analysis & Regression",
 "fn":"inertia_, percentage drop","code":"for i in range(1, len(ssd)):\n    drop = (ssd[i-1]-ssd[i])/ssd[i-1]*100\n    print(f'k={i+2}: {drop:.1f}% drop')",
 "gotcha":"Look for where percentage drop becomes small — that is the elbow.","cmp":""},
{"task":"Train a KNN Classifier","cat":"Statistical Analysis & Regression",
 "fn":"KNeighborsClassifier(), .fit()","code":"from sklearn.neighbors import KNeighborsClassifier\nknn = KNeighborsClassifier(n_neighbors=3)\nknn.fit(X_train_scaled, y_train)",
 "gotcha":"Distance-based — always standardize features. Small K overfits; large K over-smooths.","cmp":""},
{"task":"Train a KNN Regressor","cat":"Statistical Analysis & Regression",
 "fn":"KNeighborsRegressor(), .fit()","code":"from sklearn.neighbors import KNeighborsRegressor\nknn_r = KNeighborsRegressor(n_neighbors=5)\nknn_r.fit(X_train_scaled, y_train)",
 "gotcha":"Predicts the average of K nearest neighbors' target values.","cmp":""},
{"task":"Compare multiple classifiers on the same dataset","cat":"Statistical Analysis & Regression",
 "fn":"model loop","code":"for name, model in [('DT', dt), ('LR', lg), ('NB', nb)]:\n    model.fit(X_train, y_train)\n    pred = model.predict(X_test)\n    print(name, accuracy_score(y_test, pred))",
 "gotcha":"Use the same train/test split for all models for fair comparison.","cmp":""},
{"task":"Sweep a single hyperparameter and plot train vs test error","cat":"Statistical Analysis & Regression",
 "fn":"loop, accuracy_score","code":"for d in range(1, 20):\n    dt = DecisionTreeClassifier(max_depth=d)\n    dt.fit(X_train, y_train)\n    train_acc.append(dt.score(X_train, y_train))\n    test_acc.append(dt.score(X_test, y_test))",
 "gotcha":"Manual alternative to GridSearchCV for understanding one parameter.","cmp":""},
{"task":"Find frequent itemsets using the Apriori algorithm","cat":"Statistical Analysis & Regression",
 "fn":"apriori()","code":"from mlxtend.frequent_patterns import apriori\nfreq = apriori(basket.astype(bool),\n    min_support=0.02, use_colnames=True)",
 "gotcha":"Input must be boolean or 0/1 DataFrame. min_support too low = slow, too high = few results.","cmp":""},
{"task":"Generate association rules from frequent itemsets","cat":"Statistical Analysis & Regression",
 "fn":"association_rules()","code":"from mlxtend.frequent_patterns import association_rules\nrules = association_rules(freq, metric='confidence',\n    min_threshold=0.25)\nrules = rules[(rules['lift']>1) & (rules['leverage']>0)]",
 "gotcha":"High confidence alone misleads if consequent is very common. Always check lift > 1.","cmp":""},
{"task":"Build product recommendations from association rules","cat":"Statistical Analysis & Regression",
 "fn":"frozenset filtering","code":"item = frozenset(['ITEM_NAME'])\nrecs = rules[rules['antecedents']==item]\\\n    .sort_values('lift', ascending=False)",
 "gotcha":"antecedents and consequents are frozensets. Use frozenset([item]) for queries.","cmp":""},
{"task":"Find recommendations for a multi-item cart","cat":"Statistical Analysis & Regression",
 "fn":"frozenset, .issubset()","code":"cart = frozenset(['A','B'])\nrecs = rules[rules['antecedents'].apply(\n    lambda x: x.issubset(cart))]",
 "gotcha":"issubset checks if the antecedent is fully contained in the cart.","cmp":""},
{"task":"Compute association rule metrics manually","cat":"Statistical Analysis & Regression",
 "fn":"counting, arithmetic","code":"sup_A = (basket['A']==1).mean()\nsup_B = (basket['B']==1).mean()\nsup_AB = ((basket['A']==1)&(basket['B']==1)).mean()\nconf = sup_AB / sup_A\nlift = sup_AB / (sup_A * sup_B)",
 "gotcha":"Lift~1=independent. Lift>1=positive association. Leverage>0=exceeds expectation.","cmp":""},
{"task":"Encode a list of transactions into a boolean basket matrix","cat":"Statistical Analysis & Regression",
 "fn":"TransactionEncoder","code":"from mlxtend.preprocessing import TransactionEncoder\nte = TransactionEncoder()\nbasket = pd.DataFrame(te.fit_transform(transactions),\n    columns=te.columns_)",
 "gotcha":"Converts list of lists into boolean DataFrame suitable for apriori().","cmp":""},
{"task":"Interpret a decision tree node","cat":"Statistical Analysis & Regression",
 "fn":"tree visualization","code":"# Read from tree plot:\n# Split rule, samples %, value (proportions), class",
 "gotcha":"'value' shows proportions when proportion=True, otherwise raw counts.","cmp":""},
{"task":"Use weighted precision/recall/F1 for multi-class classification","cat":"Statistical Analysis & Regression",
 "fn":"precision_score(average='weighted')","code":"precision_score(y_test, y_pred, average='weighted')\nrecall_score(y_test, y_pred, average='weighted')\nf1_score(y_test, y_pred, average='weighted')",
 "gotcha":"'weighted' weights each class by its support. Use 'macro' for equal weight per class.","cmp":""},

# ── String & Text Operations ──
{"task":"Split a string by a delimiter","cat":"String & Text Operations",
 "fn":".split()","code":"'hello world'.split()\n'a,b,c'.split(',')",
 "gotcha":"split() with no argument splits on whitespace.","cmp":""},
{"task":"Slice a string to extract a substring","cat":"String & Text Operations",
 "fn":"string[start:stop]","code":"s = 'Python'\ns[0:3]  # 'Pyt'",
 "gotcha":"Slicing is exclusive of the stop index, like list slicing.","cmp":""},
{"task":"Convert a string to uppercase or lowercase","cat":"String & Text Operations",
 "fn":".upper(), .lower()","code":"'hello'.upper()  # 'HELLO'\n'HELLO'.lower()  # 'hello'",
 "gotcha":"Returns new strings; originals are immutable.","cmp":""},
{"task":"Concatenate strings with type conversion","cat":"String & Text Operations",
 "fn":"+ operator, str()","code":"'Age: ' + str(25)",
 "gotcha":"Must convert numbers to strings with str() before concatenating with +.","cmp":""},
{"task":"Count words in a text column","cat":"String & Text Operations",
 "fn":".str.split().str.len()","code":"df['word_count'] = df['text'].astype(str).str.split().str.len()",
 "gotcha":"astype(str) prevents errors if column contains NaN.","cmp":""},
{"task":"Check if a string column contains a keyword","cat":"String & Text Operations",
 "fn":".str.contains()","code":"df[df['desc'].str.contains('sale', case=False, na=False)]",
 "gotcha":"case=False = case-insensitive. na=False returns False for NaN.","cmp":""},
{"task":"Fill missing string descriptions with a fallback column","cat":"String & Text Operations",
 "fn":".fillna()","code":"df['desc'] = df['desc'].fillna(df['title'])",
 "gotcha":"fillna can accept a Series — fills NaN using values from another column row by row.","cmp":""},

# ── Other (Python basics) ──
{"task":"Perform basic arithmetic in Python","cat":"Other",
 "fn":"+ - * / // **","code":"10 / 3   # 3.333\n10 // 3  # 3\n2 ** 3   # 8",
 "gotcha":"/ always returns float. // rounds DOWN (floor), so -3//2 = -2.","cmp":""},
{"task":"Use comparison operators","cat":"Other",
 "fn":"==, !=, >=, <=","code":"x == 5\nx != 3\nx >= 10",
 "gotcha":"== checks equality; = is assignment. Common beginner mistake.","cmp":""},
{"task":"Use conditional logic with if/elif/else","cat":"Other",
 "fn":"if, elif, else","code":"if score >= 90:\n    grade = 'A'\nelif score >= 80:\n    grade = 'B'\nelse:\n    grade = 'C'",
 "gotcha":"Use and/or in if statements, not &/|. &/| are for pandas Series.","cmp":""},
{"task":"Create and manipulate a Python list","cat":"Other",
 "fn":"list, .append(), len(), indexing","code":"nums = [1, 2, 3]\nnums.append(4)\nlen(nums)  # 4\nnums[-1]   # 4",
 "gotcha":"Indexing starts at 0. Negative indices count from end: -1 is last.","cmp":""},
{"task":"Combine two lists","cat":"Other",
 "fn":"+ operator","code":"[1,2] + [3,4]  # [1,2,3,4]",
 "gotcha":"+ creates a new list; does not modify originals.","cmp":""},
{"task":"Loop through a list using range","cat":"Other",
 "fn":"for, range(), len()","code":"for i in range(len(nums)):\n    print(i, nums[i])",
 "gotcha":"range(n) produces 0..n-1. range(i,j) produces i..j-1.","cmp":""},
{"task":"Check the type of a variable","cat":"Other",
 "fn":"type()","code":"type(42)       # <class 'int'>\ntype('hello')  # <class 'str'>",
 "gotcha":"type() returns the class. Use isinstance() for type checking in conditions.","cmp":""},
{"task":"Convert between numeric types","cat":"Other",
 "fn":"float(), int(), str()","code":"float('3.14')  # 3.14\nint(3.7)       # 3\nstr(42)        # '42'",
 "gotcha":"int() truncates toward zero, does not round. int(-3.7) = -3.","cmp":""},
{"task":"Define a reusable function","cat":"Other",
 "fn":"def, return","code":"def greet(name):\n    return 'Hello ' + name",
 "gotcha":"Functions must be defined before called. return sends output back.","cmp":""},
]

confused_pairs = [
("iloc vs loc", "iloc uses integer positions (exclusive end); loc uses label names (inclusive end)."),
("head() vs tail()", "head() shows first N rows; tail() shows last N rows."),
("info() vs describe()", "info() shows column types and non-null counts; describe() shows numeric summary statistics."),
("fillna() vs dropna()", "fillna() replaces missing values; dropna() removes rows/columns with missing values."),
("value_counts() vs nunique()", "value_counts() returns counts per unique value; nunique() returns just the count of distinct values."),
("unique() vs nunique()", "unique() returns the actual distinct values; nunique() returns how many there are."),
("pd.concat() vs pd.merge()", "concat joins by index (axis=0 rows, axis=1 columns); merge joins by matching key column values."),
("axis=0 vs axis=1", "axis=0 operates along rows (vertically); axis=1 operates along columns (horizontally)."),
("predict() vs predict_proba()", "predict() returns class labels; predict_proba() returns probability estimates for each class."),
("fit_transform() vs transform()", "fit_transform() learns parameters and transforms (training); transform() applies learned parameters (test)."),
("get_dummies() vs LabelEncoder", "get_dummies creates multiple 0/1 columns (one-hot); LabelEncoder assigns a single integer per category."),
("DecisionTreeClassifier vs Regressor", "Classifier predicts categories (accuracy/F1); Regressor predicts numbers (MAE/RMSE/R2)."),
("KNeighborsClassifier vs Regressor", "Classifier predicts majority class among K neighbors; Regressor predicts average target of K neighbors."),
("Linear vs Logistic Regression", "Linear predicts a continuous number (minimizes squared error); logistic predicts class probability (maximizes likelihood)."),
("Naive Bayes vs Logistic Regression", "Naive Bayes assumes feature independence and learns distributions; logistic regression directly models the decision boundary."),
("StratifiedKFold vs KFold", "StratifiedKFold preserves class proportions (classification); KFold does not (regression)."),
("cross_validate() vs cross_val_predict()", "cross_validate returns metric scores per fold; cross_val_predict returns actual out-of-fold predictions."),
("GridSearchCV vs manual sweep", "GridSearchCV automates all combinations with CV; manual sweep loops over one parameter."),
("Support vs Confidence vs Lift", "Support = frequency of itemset; Confidence = P(B|A); Lift = observed/expected co-occurrence."),
("K-means vs KNN", "K-means is unsupervised clustering; KNN is supervised prediction using nearest labeled neighbors."),
("Pre-pruning vs Post-pruning", "Pre-pruning sets limits before training (max_depth); post-pruning (ccp_alpha) removes branches after."),
("MAE vs RMSE", "MAE treats all errors equally; RMSE penalizes large errors more."),
("and/or vs &/|", "Use and/or in Python if/else; use &/| for element-wise pandas Series operations (with parentheses)."),
("transform() vs agg()", "transform broadcasts group result back to every original row; agg collapses each group into one row."),
]

concepts = [
{"title":"Supervised vs Unsupervised Learning","cat":"Statistical Analysis & Regression",
 "body":"Supervised: target variable y to predict. Unsupervised: no target, discover patterns. Decision Trees, Linear/Logistic Regression, KNN, Naive Bayes are supervised. K-means and Association Rules are unsupervised."},
{"title":"What is Overfitting and How to Reduce It","cat":"Statistical Analysis & Regression",
 "body":"Model memorizes training noise. Signs: low train error, high test error. Pre-pruning: max_depth, min_samples_split, min_samples_leaf, max_leaf_nodes, max_features. Post-pruning: ccp_alpha."},
{"title":"How to Read a Decision Tree Node","cat":"Statistical Analysis & Regression",
 "body":"Each node: (1) Split rule e.g. Age<=42.5. (2) samples = % of data. (3) value = class distribution. (4) class = majority prediction. proportion=True shows proportions."},
{"title":"Entropy vs Gini Impurity","cat":"Statistical Analysis & Regression",
 "body":"criterion='entropy' uses information gain. 'gini' (default) uses Gini impurity. Usually similar trees. Entropy tends to produce slightly more balanced splits."},
{"title":"Classification Metrics","cat":"Statistical Analysis & Regression",
 "body":"Accuracy=(TP+TN)/total. Precision=TP/(TP+FP). Recall=TP/(TP+FN). F1=harmonic mean. ROC AUC ranks positives above negatives. Confusion matrix: rows=actual, cols=predicted."},
{"title":"Regression Metrics","cat":"Statistical Analysis & Regression",
 "body":"MAE=avg|actual-predicted|. RMSE=sqrt(avg squared errors), penalizes large errors. R2=variance explained. R2=1 perfect, 0=no better than mean, <0=worse."},
{"title":"Cross-Validation","cat":"Statistical Analysis & Regression",
 "body":"K-fold: train on k-1 folds, validate on held-out fold, rotate k times. More reliable than single split. When tuning with GridSearchCV, tune on train only, evaluate best on test."},
{"title":"StratifiedKFold vs KFold","cat":"Statistical Analysis & Regression",
 "body":"StratifiedKFold preserves class proportions — use for classification. KFold does not — use for regression."},
{"title":"GridSearchCV Workflow","cat":"Statistical Analysis & Regression",
 "body":"Tries every param_grid combination with k-fold CV. refit= selects best metric. best_estimator_ refit on full train. Evaluate once on test. n_jobs=-1 for all cores."},
{"title":"Why Standardize Features","cat":"Data Cleaning & Preprocessing",
 "body":"X_std=(X-mean)/std. Distance-based methods (KNN, K-means) dominated by large-scale features. Regularized models affected by scale. After standardization, coefficients comparable."},
{"title":"Why Log-Transform Skewed Features","cat":"Data Cleaning & Preprocessing",
 "body":"Skewed: most small, few very large. GaussianNB works better with bell-shaped. log1p(x)=log(1+x) shrinks extremes. Safe for zeros. Cannot handle negatives. |skew|>3 = strong."},
{"title":"Feature Engineering Rationale","cat":"Data Cleaning & Preprocessing",
 "body":"Create new predictors from existing columns. Add small constant to denominators. Linear regression is linear in parameters — can add log, polynomial, interaction terms. More features != better."},
{"title":"One-Hot Encoding Explained","cat":"Data Cleaning & Preprocessing",
 "body":"Most sklearn models need numbers. One-hot: categorical → multiple 0/1 columns. drop_first=True avoids multicollinearity. For 2-value columns, .map() to 0/1 is simpler."},
{"title":"Linear Regression Concepts","cat":"Statistical Analysis & Regression",
 "body":"y_hat = theta_0 + theta_1*x1 + ... Minimizes squared errors (OLS). Positive coef = increases prediction. Coefficients comparable only after standardization. No hyperparameters."},
{"title":"Logistic Regression Concepts","cat":"Statistical Analysis & Regression",
 "body":"Predicts P(y=1). Class 1 if prob >= 0.5. Learned by MLE = minimizing log loss. Increase max_iter if convergence warning. predict_proba()[:,1] for positive class."},
{"title":"Naive Bayes Concepts","cat":"Statistical Analysis & Regression",
 "body":"Learns feature distributions per class. Combines evidence for class probability. 'Naive' = assumes independence given class. Sensitive to scale. Interpret by comparing feature means."},
{"title":"K-Means Clustering","cat":"Statistical Analysis & Regression",
 "body":"Unsupervised. Groups into k clusters minimizing SSD/inertia. Always standardize. Elbow Method: plot SSD vs k. n_init=10 runs 10 times. Interpret via cluster profiles."},
{"title":"KNN Concepts","cat":"Statistical Analysis & Regression",
 "body":"Memory-based. Classification: majority class. Regression: average target. Always standardize. Small K overfits, large K over-smooths. KNN is supervised (unlike K-means)."},
{"title":"Association Rules","cat":"Statistical Analysis & Regression",
 "body":"Unsupervised, counting co-occurrences. Support=frequency. Confidence=P(B|A). Lift=observed/expected. Lift>1=positive. HIGH CONFIDENCE CAN MISLEAD when consequent common. Check lift."},
{"title":"Apriori Algorithm","cat":"Statistical Analysis & Regression",
 "body":"If itemset NOT frequent, no superset can be. Prunes search space. Workflow: (1) frequent itemsets (min support). (2) rules (min confidence). (3) filter lift>1."},
{"title":"Train/Test Split Purpose","cat":"Statistical Analysis & Regression",
 "body":"Estimates generalization. test_size=0.2. random_state=reproducible. stratify=y for classification. When using GridSearchCV, tune on train, evaluate on test."},
{"title":"Comparing Multiple Models","cat":"Statistical Analysis & Regression",
 "body":"Same pattern: fit, predict, predict_proba. Same split for fair comparison. Hardest part is often cleaning data and feature engineering, not the model."},
{"title":"Predicted vs Actual Plot","cat":"Visualization",
 "body":"Diagonal = perfect. Points close = good. Systematic curves = model missing nonlinear relationship."},
{"title":"ROC Curve","cat":"Visualization",
 "body":"TPR vs FPR at different thresholds. Perfect=top-left (AUC=1). Random=diagonal (AUC=0.5). Needs probabilities."},
{"title":"Complexity Curve","cat":"Visualization",
 "body":"Train/test error vs complexity. Train decreases. Test decreases then increases = overfitting. Sweet spot = lowest test error."},
{"title":"Elbow Method","cat":"Visualization",
 "body":"SSD vs k. Always decreases. Look for bend where adding clusters gives diminishing returns."},
{"title":"Data Exploration Workflow","cat":"Data Import & File I/O",
 "body":"df.info() for types/nulls, df.describe() for stats, df.shape for dimensions, value_counts() for categories, isnull().sum() for missing. Histograms + heatmaps."},
{"title":"Comparing Groups","cat":"Data Selection & Filtering",
 "body":"Filter subsets with df.loc. Compare describe(). Check median and 75%. Plot histograms. Use value_counts(normalize=True)."},
]

# ══════════════════════════════════════════════════════════════
#  GENERATE review.html
# ══════════════════════════════════════════════════════════════
from collections import defaultdict

by_cat = defaultdict(list)
for e in entries:
    by_cat[e["cat"]].append(e)

concepts_by_cat = defaultdict(list)
for c in concepts:
    concepts_by_cat[c["cat"]].append(c)

review_lines = []
review_lines.append("""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>MM5425 Quick Review</title>
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#fff;color:#333;line-height:1.6;padding:20px;max-width:900px;margin:0 auto}
.nav{text-align:center;margin-bottom:12px;font-size:14px}
.nav a{color:#4a6fa5;text-decoration:none;font-weight:600}
h1{text-align:center;color:#2c3e50;margin-bottom:4px;font-size:1.5em}
.sub{text-align:center;color:#666;margin-bottom:20px;font-size:.9em}
h2{color:#2c3e50;border-bottom:2px solid #4a6fa5;padding-bottom:4px;margin:24px 0 12px;font-size:1.15em}
table{width:100%;border-collapse:collapse;margin-bottom:16px;font-size:.88em}
th{background:#4a6fa5;color:#fff;padding:6px 10px;text-align:left;font-weight:600}
td{padding:6px 10px;border-bottom:1px solid #e0e0e0;vertical-align:top}
tr:nth-child(even){background:#f8f9fb}
.fn{font-family:Consolas,'SFMono-Regular',monospace;font-size:.85em;color:#4527a0}
.go{color:#b71c1c;font-size:.85em}
.confused{margin-top:30px}
.confused table td:first-child{font-weight:600;white-space:nowrap;width:30%}
.concept{background:#eef2ff;border-left:3px solid #4a6fa5;padding:6px 10px;margin:4px 0 8px;font-size:.86em;border-radius:0 4px 4px 0;line-height:1.5}
.concept-title{font-weight:700;color:#2c3e50}
@media print{body{padding:10px;font-size:11px}h1{font-size:1.3em}h2{font-size:1em;margin:14px 0 8px}table{font-size:.8em;page-break-inside:auto}td,th{padding:4px 6px}tr{page-break-inside:avoid}}
</style></head><body>
<div class="nav"><a href="repository.html">&#8594; Code Repository</a></div>
<h1>MM5425 Quick Review Sheet</h1>
<p class="sub">One-page mental walkthrough &mdash; what tool for what job</p>""")

for cat in CAT_ORDER:
    rows = by_cat.get(cat, [])
    cat_concepts = concepts_by_cat.get(cat, [])
    if not rows and not cat_concepts:
        continue
    review_lines.append(f'<h2>{esc(cat)}</h2>')
    # Render concept cards for this category
    if cat_concepts:
        for c in cat_concepts:
            review_lines.append(f'<div class="concept"><span class="concept-title">{esc(c["title"])}</span> &mdash; {esc(c["body"])}</div>')
    # Render task table
    if rows:
        review_lines.append('<table><tr><th>Task</th><th>Key Functions</th><th>Gotcha</th></tr>')
        for e in rows:
            review_lines.append(f'<tr><td>{esc(e["task"])}</td><td class="fn">{esc(e["fn"])}</td><td class="go">{esc(e.get("gotcha",""))}</td></tr>')
        review_lines.append('</table>')

review_lines.append('<div class="confused"><h2>Commonly Confused Pairs</h2>')
review_lines.append('<table><tr><th>Pair</th><th>Distinction</th></tr>')
for pair, dist in confused_pairs:
    review_lines.append(f'<tr><td>{esc(pair)}</td><td>{esc(dist)}</td></tr>')
review_lines.append('</table></div>\n</body></html>')

with open('review.html', 'w') as f:
    f.write('\n'.join(review_lines))
print(f"Generated review.html")

# ══════════════════════════════════════════════════════════════
#  GENERATE repository.html
# ══════════════════════════════════════════════════════════════
import json as JSON

# Build JSON data for JS
cards_json = JSON.dumps(entries, ensure_ascii=False)

repo_html = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>MM5425 Code Repository</title>
<style>
"""

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;background:#f5f6fa;color:#333;line-height:1.6;padding:20px;max-width:960px;margin:0 auto}
.nav{text-align:center;margin-bottom:8px;font-size:14px}
.nav a{color:#4a6fa5;text-decoration:none;font-weight:600}
h1{text-align:center;color:#2c3e50;margin-bottom:4px;font-size:1.5em}
.sub{text-align:center;color:#666;margin-bottom:16px;font-size:.9em}
#search{width:100%;padding:10px 14px;font-size:15px;border:2px solid #ccc;border-radius:8px;margin-bottom:10px;outline:none}
#search:focus{border-color:#4a6fa5}
.filters{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px;justify-content:center}
.fbtn{padding:4px 12px;border:1px solid #bbb;border-radius:16px;background:#fff;cursor:pointer;font-size:13px;transition:.2s}
.fbtn:hover{background:#e8edf3}
.fbtn.active{background:#4a6fa5;color:#fff;border-color:#4a6fa5}
#count{text-align:center;color:#666;font-size:13px;margin-bottom:14px}
.card{background:#fff;border:1px solid #e0e0e0;border-radius:8px;margin-bottom:10px;overflow:hidden;transition:.2s}
.card.hidden{display:none}
.card-head{padding:10px 14px;cursor:pointer;display:flex;align-items:flex-start;gap:10px}
.card-head:hover{background:#f0f4f8}
.arrow{font-size:12px;color:#999;flex-shrink:0;margin-top:3px;transition:transform .2s}
.card.open .arrow{transform:rotate(90deg)}
.card-title{flex:1;font-weight:600;font-size:.95em}
.badge{display:inline-block;padding:1px 8px;border-radius:10px;font-size:11px;font-weight:600;color:#fff;margin-left:6px;flex-shrink:0}
.card-fn{font-family:Consolas,'SFMono-Regular',monospace;font-size:.82em;color:#4527a0;padding:0 14px 8px 38px}
.card-body{display:none;padding:0 14px 14px 14px;border-top:1px solid #eee}
.card.open .card-body{display:block}
.card-body pre{background:#1e1e2e;color:#cdd6f4;padding:12px;border-radius:6px;overflow-x:auto;font-size:13px;line-height:1.5;margin:8px 0}
.card-body pre .kw{color:#cba6f7}.card-body pre .fn2{color:#89b4fa}.card-body pre .st{color:#a6e3a1}.card-body pre .cm{color:#6c7086;font-style:italic}.card-body pre .num{color:#fab387}.card-body pre .op{color:#f38ba8}
.gotcha{background:#fff8e1;border-left:3px solid #f9a825;padding:6px 10px;margin:6px 0;font-size:.88em;border-radius:0 4px 4px 0}
.cmp{font-size:.85em;color:#555;margin-top:4px;font-style:italic}
@media print{.card-body{display:block!important}.filters,#search{display:none}}
"""

BADGE_COLORS = {
    "Data Import & File I/O":"#2196f3",
    "Data Cleaning & Preprocessing":"#4caf50",
    "Data Selection & Filtering":"#ff9800",
    "Aggregation & Grouping":"#9c27b0",
    "Merging & Joining":"#00bcd4",
    "Reshaping & Pivoting":"#795548",
    "Visualization":"#e91e63",
    "Statistical Analysis & Regression":"#3f51b5",
    "String & Text Operations":"#607d8b",
    "Other":"#9e9e9e",
}

import re

def highlight_code(code):
    """Very basic syntax highlighting via regex on raw code, then escape the text parts."""
    tokens = []  # list of (text, css_class_or_None)

    # Regex that captures comments, strings, keywords, numbers — in priority order
    kw_list = r'import|from|for|in|if|elif|else|def|return|as|not|and|or|True|False|None|print|lambda'
    pattern = re.compile(
        r'(#[^\n]*)'                          # group 1: comment
        r"|('(?:[^'\\]|\\.)*'|\"(?:[^\"\\]|\\.)*\")"  # group 2: string
        r'|(\b(?:' + kw_list + r')\b)'        # group 3: keyword
        r'|(\b\d+\.?\d*\b)'                   # group 4: number
    )

    last = 0
    for m in pattern.finditer(code):
        # plain text before this match
        if m.start() > last:
            tokens.append((code[last:m.start()], None))
        if m.group(1):
            tokens.append((m.group(1), "cm"))
        elif m.group(2):
            tokens.append((m.group(2), "st"))
        elif m.group(3):
            tokens.append((m.group(3), "kw"))
        elif m.group(4):
            tokens.append((m.group(4), "num"))
        last = m.end()
    # trailing plain text
    if last < len(code):
        tokens.append((code[last:], None))

    # Build HTML: escape each token's text, then wrap with span if needed
    parts = []
    for text, cls in tokens:
        escaped = esc(text)
        if cls:
            parts.append(f'<span class="{cls}">{escaped}</span>')
        else:
            parts.append(escaped)
    return "".join(parts)

def build_card_html(e, idx):
    cat = e["cat"]
    color = BADGE_COLORS.get(cat, "#999")
    code_hl = highlight_code(e.get("code",""))
    gotcha_html = f'<div class="gotcha">{esc(e["gotcha"])}</div>' if e.get("gotcha") else ""
    cmp_html = f'<div class="cmp">{esc(e["cmp"])}</div>' if e.get("cmp") else ""
    return f'''<div class="card" data-cat="{esc(cat)}" data-search="{esc((e["task"]+" "+e["fn"]+" "+e.get("gotcha","")+" "+e.get("code","")+" "+cat).lower())}">
<div class="card-head" onclick="toggle(this)"><span class="arrow">&#9654;</span><span class="card-title">{esc(e["task"])}</span><span class="badge" style="background:{color}">{esc(cat)}</span></div>
<div class="card-fn">{esc(e["fn"])}</div>
<div class="card-body"><pre>{code_hl}</pre>{gotcha_html}{cmp_html}</div></div>'''

cards_html = "\n".join(build_card_html(e, i) for i, e in enumerate(entries))

filter_btns = '<button class="fbtn active" onclick="filterCat(this,\'all\')">All</button>\n'
for cat in CAT_ORDER:
    color = BADGE_COLORS.get(cat, "#999")
    filter_btns += f'<button class="fbtn" onclick="filterCat(this,\'{esc(cat)}\')" style="border-color:{color}">{esc(cat)}</button>\n'

JS = """
let activeCat='all';
function filterCat(btn,cat){
  activeCat=cat;
  document.querySelectorAll('.fbtn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  applyFilters();
}
function applyFilters(){
  const q=document.getElementById('search').value.toLowerCase();
  let n=0;
  document.querySelectorAll('.card').forEach(c=>{
    const catMatch=activeCat==='all'||c.dataset.cat===activeCat;
    const txtMatch=!q||c.dataset.search.includes(q);
    if(catMatch&&txtMatch){c.classList.remove('hidden');n++}
    else{c.classList.add('hidden')}
  });
  document.getElementById('count').textContent=n+' entries shown';
}
function toggle(el){el.parentElement.classList.toggle('open')}
document.getElementById('search').addEventListener('input',applyFilters);
window.addEventListener('DOMContentLoaded',applyFilters);
"""

repo_full = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>MM5425 Code Repository</title>
<style>{CSS}</style></head><body>
<div class="nav"><a href="review.html">&#8594; Quick Review Sheet</a></div>
<h1>MM5425 Searchable Code Repository</h1>
<p class="sub">Every technique from all 10 tutorial files &mdash; search, filter, expand</p>
<input id="search" type="text" placeholder="Search tasks, functions, code, gotchas...">
<div class="filters">{filter_btns}</div>
<div id="count"></div>
{cards_html}
<script>{JS}</script>
</body></html>"""

with open('repository.html', 'w') as f:
    f.write(repo_full)
print(f"Generated repository.html ({len(entries)} entries)")
