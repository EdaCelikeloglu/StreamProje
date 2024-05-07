import plotly.express as px
import streamlit as st
import time
import numpy as np
import networkx as nx
import plotly.graph_objects as go
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.impute import KNNImputer
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import OrdinalEncoder
from main import process_data
import warnings
warnings.simplefilter(action="ignore")



st.set_page_config(page_title="Plotting Demo", page_icon="📈", layout="wide")

st.markdown("# Plotting Demo")
st.sidebar.header("Plotting Demo")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)
# def process_data(df):
#     # Fonksiyonlarımız:
#     def grab_col_names(dataframe, cat_th=9, car_th=20):
#         #cat_cols, cat_but_car
#         cat_cols = [col for col in dataframe.columns if dataframe[col].dtypes == "O"]
#         num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and
#                        dataframe[col].dtypes != "O"]
#         cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > car_th and
#                        dataframe[col].dtypes == "O"]
#         cat_cols = cat_cols + num_but_cat
#         cat_cols = [col for col in cat_cols if col not in cat_but_car]
#
#         #num_cols
#         num_cols = [col for col in dataframe.columns if dataframe[col].dtypes != "O"]
#         num_cols = [col for col in num_cols if col not in num_but_cat]
#
#         return cat_cols, num_cols, cat_but_car
#
#     def outlier_thresholds(dataframe, col_name, q1=0.05, q3=0.95):
#         quartile1 = dataframe[col_name].quantile(q1)
#         quartile3 = dataframe[col_name].quantile(q3)
#         interquantile_range = quartile3 - quartile1
#         up_limit = quartile3 + 1.5 * interquantile_range
#         low_limit = quartile1 - 1.5 * interquantile_range
#         return low_limit, up_limit
#
#     def check_outlier(dataframe, col_name):
#         low_limit, up_limit = outlier_thresholds(dataframe, col_name)
#         if dataframe[(dataframe[col_name] > up_limit) | (dataframe[col_name] < low_limit)].any(axis=None):
#             return True
#         else:
#             return False
#
#     def grab_outliers(dataframe, col_name, index=False):
#         low, up = outlier_thresholds(dataframe, col_name)
#         if index:
#             outlier_index = dataframe[((dataframe[col_name] < low) | (dataframe[col_name] > up))].index
#             return outlier_index
#
#     def replace_with_thresholds(dataframe, variable):
#         low_limit, up_limit = outlier_thresholds(dataframe, variable)
#         dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
#         dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit
#
#     def cat_summary(dataframe, col_name, plot=False):
#         print(pd.DataFrame({col_name: dataframe[col_name].value_counts(),
#                             "Ratio": 100 * dataframe[col_name].value_counts() / len(dataframe)}))
#         print("##########################################")
#         if plot:
#             sns.countplot(x=dataframe[col_name], data=dataframe)
#             plt.show(block=True)
#
#     def num_summary(dataframe, numerical_col, plot=False):
#         quantiles = [0.05, 0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 0.95, 0.99]
#         print(dataframe[numerical_col].describe(quantiles).T)
#
#         if plot:
#             dataframe[numerical_col].hist(bins=20)
#             plt.xlabel(numerical_col)
#             plt.title(numerical_col)
#             plt.show(block=True)
#
#     def one_hot_encoder(dataframe, categorical_cols, drop_first=True):
#         dataframe = pd.get_dummies(dataframe, columns=categorical_cols, drop_first=drop_first, dtype=int)
#         return dataframe
#
#     def combine_categories(df, cat_col1, cat_col2, new_col_name):
#         df[new_col_name] = df[cat_col1].astype(str) + '_' + df[cat_col2].astype(str)
#
#     df.drop([
#         "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_1",
#         "Naive_Bayes_Classifier_Attrition_Flag_Card_Category_Contacts_Count_12_mon_Dependent_count_Education_Level_Months_Inactive_12_mon_2"],
#         inplace=True, axis=1)
#
#     # Bağımlı değişkenimizin ismini target yapalım ve 1, 0 atayalım:
#     df.rename(columns={"Attrition_Flag": "Target"}, inplace=True)
#     df["Target"] = df.apply(lambda x: 0 if (x["Target"] == "Existing Customer") else 1, axis=1)
#
#     # ID kolonunda duplicate bakıp, sonra bu değişkeni silme
#     df["CLIENTNUM"].nunique()  # 10127 - yani duplicate yok id'de
#     df.drop("CLIENTNUM", axis=1, inplace=True)
#
#     cat_cols, num_cols, cat_but_car = grab_col_names(df)
#
#
#     # LOF
#     clf = LocalOutlierFactor(n_neighbors=20)
#     clf.fit_predict(df[num_cols])
#
#     df_scores = clf.negative_outlier_factor_
#
#     scores = pd.DataFrame(np.sort(df_scores))
#     scores.plot(stacked=True, xlim=[0, 100], style='.-')
#     plt.show()
#
#     th = np.sort(df_scores)[25]
#
#     outliers = df_scores < th
#     #df = df[~outliers]
#
#
#     cat_cols, num_cols, cat_but_car = grab_col_names(df)
#     # Missing values
#     cols_with_unknown = ['Income_Category', "Education_Level"]
#     for col in cols_with_unknown:
#         df[col] = df[col].apply(lambda x: np.nan if x == 'Unknown' else x)
#
#     df["On_book_cat"] = np.where((df["Months_on_book"] < 12), "<1_year", np.where((df["Months_on_book"] < 24), "<2_years", np.where((df["Months_on_book"] < 36), "<3_years", np.where((df["Months_on_book"] < 48), "<4_years", "<5_years"))))
#     df['Total_Amt_Increased'] = np.where((df['Total_Amt_Chng_Q4_Q1'] > 0) & (df['Total_Amt_Chng_Q4_Q1'] < 1), 0, 1)
#     df["Has_debt"] = np.where((df["Credit_Limit"] > df["Avg_Open_To_Buy"]), 1, 0).astype(int)
#     df["Important_client_score"] = df["Total_Relationship_Count"] * (df["Months_on_book"] / 12)
#     df["Avg_Trans_Amt"] = df["Total_Trans_Amt"] / df['Total_Trans_Ct']
#
#     labels = ['Young', 'Middle_Aged', 'Senior']
#     bins = [25, 35, 55, 74]
#     df['Customer_Age_Category'] = pd.cut(df['Customer_Age'], bins=bins, labels=labels)
#
#     df["Days_Inactive_Last_Year"] = df["Months_Inactive_12_mon"] * 30
#     df["Days_Inactive_Last_Year"].value_counts()
#
#
#     df["Days_Inactive_Last_Year"].replace(0, 30, inplace=True)
#     df["Days_Inactive_Last_Year"].replace(180, 150, inplace=True)
#
#
#     # RFM
#     df["RecencyScore"] = df["Days_Inactive_Last_Year"].apply(lambda x: 5 if x == 30 else
#                                                             4 if x == 60 else
#                                                             3 if x == 90 else
#                                                             2 if x == 120 else
#                                                             1 if x == 150 else x)
#
#     df["MonetaryScore"] = pd.qcut(df["Total_Trans_Amt"], 5, labels=[1, 2, 3, 4, 5])
#     df["FrequencyScore"] = pd.qcut(df["Total_Trans_Ct"], 5, labels=[1, 2, 3, 4, 5])
#
#     seg_map = {
#             r'[1-2][1-2]': 'Hibernating',
#             r'[1-2][3-4]': 'At Risk',
#             r'[1-2]5': 'Can\'t Lose',
#             r'3[1-2]': 'About to Sleep',
#             r'33': 'Need Attention',
#             r'[3-4][4-5]': 'Loyal Customers',
#             r'41': 'Promising',
#             r'51': 'New Customers',
#             r'[4-5][2-3]': 'Potential Loyalists',
#             r'5[4-5]': 'Champions'
#     }
#
#     # segment oluşturma (Recency + Frequency)
#     df['Segment'] = df['RecencyScore'].astype(str) + df['FrequencyScore'].astype(str)
#     df['Segment'] = df['Segment'].replace(seg_map, regex=True)
#     df.head(40)
#
#
#     # k-means ile müşteri segmentasyonu öncesi standartlaştırmayı yapmak gerek
#     # Min-Max ölçeklendirme
#     from sklearn.preprocessing import MinMaxScaler
#
#
#     sc = MinMaxScaler((0,1))
#     df[['Days_Inactive_Last_Year','Total_Trans_Ct', 'Total_Trans_Amt']] = sc.fit_transform(df[['Days_Inactive_Last_Year', 'Total_Trans_Ct', 'Total_Trans_Amt']])
#
#
#     from sklearn.cluster import KMeans
#     # model fit edildi.
#     kmeans = KMeans(n_clusters = 4, max_iter=50)
#     kmeans.fit(df[['Days_Inactive_Last_Year','Total_Trans_Ct', 'Total_Trans_Amt']])
#
#     df["cluster_no"] = kmeans.labels_
#     df["cluster_no"] = df["cluster_no"] + 1
#
#
#     ssd = []
#
#     K = range(1,30)
#
#     for k in K:
#         kmeans = KMeans(n_clusters=k).fit(df[['Days_Inactive_Last_Year', 'Total_Trans_Ct', 'Total_Trans_Amt']])
#         ssd.append(kmeans.inertia_) #inertia her bir k değeri için ssd değerini bulur.
#
#
#     # Optimum küme sayısını belirleme
#     from yellowbrick.cluster import KElbowVisualizer
#     kmeans = KMeans()
#     elbow = KElbowVisualizer(kmeans, k=(2, 20))
#     elbow.fit(df[['Days_Inactive_Last_Year', 'Total_Trans_Ct', 'Total_Trans_Amt']])
#     elbow.show()
#     elbow.elbow_value_
#
#
#     # yeni optimum küme sayısı ile model fit edilmiştir.
#     kmeans = KMeans(n_clusters = elbow.elbow_value_).fit(df[['Days_Inactive_Last_Year', 'Total_Trans_Ct', 'Total_Trans_Amt']])
#
#
#     # Cluster_no 0'dan başlamaktadır. Bunun için 1 eklenmiştir.
#     df["cluster_no"] = kmeans.labels_
#     df["cluster_no"] = df["cluster_no"] + 1
#
#
#
#     combine_categories(df, 'Customer_Age_Category', 'Marital_Status', 'Age_&_Marital')
#     combine_categories(df, 'Gender', 'Customer_Age_Category', 'Gender_&_Age')
#     combine_categories(df, "Card_Category", "Customer_Age_Category", "Card_&_Age")
#     combine_categories(df, "Gender", "FrequencyScore", "Gender_&_Frequency")
#     combine_categories(df, "Gender", "MonetaryScore", "Gender_&_Monetary")
#
#     df['Total_Amt_Increased'] = np.where((df['Total_Amt_Chng_Q4_Q1'] >= 0) & (df['Total_Amt_Chng_Q4_Q1'] < 1), 0, 1)
#     df['Total_Ct_Increased'] = np.where((df['Total_Ct_Chng_Q4_Q1'] >= 0) & (df['Total_Ct_Chng_Q4_Q1'] < 1), 0, 1)
#
#
#     # İşlem sayısı ve miktarı pattern'leri:
#     # İşlem sayısı aynı kalıp, harcama miktarı artanlar: (belki daha çok para kazanmaya başlamışlardır)(TODO kredi limiti ile incele)
#     df.loc[(df["Total_Ct_Chng_Q4_Q1"] == 1) & (df["Total_Amt_Chng_Q4_Q1"] > 1), "Ct_vs_Amt"] = "Same_ct_inc_amt"
#     # boş
#     df.loc[(df["Total_Ct_Chng_Q4_Q1"] == 1) & (df["Total_Amt_Chng_Q4_Q1"] == 1), "Ct_vs_Amt"] = "Same_ct_same_amt" # BOŞ
#     # İşlem sayısı aynı kalıp, harcama miktarı azalanlar: (harcamalardan mı kısıyorlar? belki ihtiyaçları olanları almışlardır.) TODO May_Marry ile incele)
#     df.loc[(df["Total_Ct_Chng_Q4_Q1"] == 1) & (df["Total_Amt_Chng_Q4_Q1"] < 1), "Ct_vs_Amt"] = "Same_ct_dec_amt"
#     # işlem sayısı da, miktarı da artmış (bizi sevindiren müşteri <3 )
#     df.loc[(df["Total_Ct_Chng_Q4_Q1"] > 1) & (df["Total_Amt_Chng_Q4_Q1"] > 1), "Ct_vs_Amt"] = "Inc_ct_inc_amt"
#     # BOŞ İşlem sayısı artmasına rağmen, harcama miktarı aynı kalanlar: (aylık ortalama harcama azalıyor)
#     df.loc[(df["Total_Ct_Chng_Q4_Q1"] > 1) & (df["Total_Amt_Chng_Q4_Q1"] == 1), "Ct_vs_Amt"] = "Inc_ct_same_amt" # BOŞ
#     # İşlem sayısı artmış ama miktar azalmış. Yani daha sık, ama daha küçük alışverişler yapıyor. Bunlar düşük income grubuna aitse bankayı mutlu edecek bir davranış.
#     df.loc[(df["Total_Ct_Chng_Q4_Q1"] > 1) & (df["Total_Amt_Chng_Q4_Q1"] < 1), "Ct_vs_Amt"] = "Inc_ct_dec_amt"
#     #(df.loc[(df["Total_Ct_Chng_Q4_Q1"] > 1) & (df["Total_Amt_Chng_Q4_Q1"] < 1)]).groupby("Income_Category").count() # Evet, düşük income grubuna ait.
#     # İşlem sayısı azalmış ama daha büyük miktarlarda harcama yapılıyor:
#     df.loc[(df["Total_Ct_Chng_Q4_Q1"] < 1) & (df["Total_Amt_Chng_Q4_Q1"] > 1), "Ct_vs_Amt"] = "Dec_ct_inc_amt"
#     # İşlem sayısı azalmış, toplam miktar aynı kalmış (yani ortalama harcama artmış):
#     df.loc[(df["Total_Ct_Chng_Q4_Q1"] < 1) & (df["Total_Amt_Chng_Q4_Q1"] == 1), "Ct_vs_Amt"] = "Dec_ct_same_amt"
#     # İşlem sayısı azalmış, miktar da azalmış. Churn eder mi acaba?
#     df.loc[(df["Total_Ct_Chng_Q4_Q1"] < 1) & (df["Total_Amt_Chng_Q4_Q1"] < 1), "Ct_vs_Amt"] = "Dec_ct_dec_amt"
#     # (df.loc[(df["Total_Ct_Chng_Q4_Q1"] < 1) & (df["Total_Amt_Chng_Q4_Q1"] < 1)])["Target"].mean() # 0.17
#
#
#     # Personalar
#     df["Affluent_criteria"] = (df['Income_Category'] == '$120K +').astype('Int64')
#     df["Budget_criteria"] = ((df['Income_Category'] == 'Less than $40K') & (df['Education_Level'].isin(['High School', 'College']))).astype('Int64')
#     df["Young_prof_criteria"] = ((df['Customer_Age'] <= 30) & (df['Education_Level'].isin(['College', 'Graduate']))).astype('Int64')
#     df["Family_criteria"] = ((df["Marital_Status"].isin(["Married", "Divorced", "Unknown"])) & (df['Dependent_count'] >= 3)).astype(int)
#     df["Credit_builder_criteria"] = (df['Credit_Limit'] < 2500).astype(int)  # This threshold is chosen to include individuals with credit limits in the lower percentiles of the distribution, which may indicate a need for credit-building strategies or entry-level credit products.
#     df["Digital_criteria"] = (df['Contacts_Count_12_mon'] == 0).astype(int)
#     df["High_net_worth_individual"] = ((df['Income_Category'] == '$120K +') & (df['Total_Trans_Amt'] > 5000)).astype('Int64')
#     df["Rewards_maximizer"] = ((df['Total_Trans_Amt'] > 10000) & (df['Total_Revolving_Bal'] == 0)).astype(int) # For the Rewards_maximizer column, the threshold for Total_Trans_Amt is also set at $10000. Since rewards maximizers are individuals who strategically maximize rewards and benefits from credit card usage, it's reasonable to expect that they engage in higher levels of spending. Therefore, the threshold of $10000 for Total_Trans_Amt appears appropriate for identifying rewards maximizers, considering that it captures individuals with relatively high spending habits.
#     df["May_marry"] = ((df["Age_&_Marital"] == "Young_Single") & (df['Dependent_count'] == 0)).astype(int)
#
#
#     df["Product_by_Year"] = df["Total_Relationship_Count"] / (df["Months_on_book"] / 12)
#     df['Year_on_book'] = df['Months_on_book'] // 12
#
#     cat_cols, num_cols, cat_but_car = grab_col_names(df)
#
#     # Encoding:
#     # Rare encoding:
#     df["Card_Category"] = df["Card_Category"].apply(lambda x: "Gold_Platinum" if x == "Platinum" or x == "Gold" else x)
#     df["Months_Inactive_12_mon"] = df["Months_Inactive_12_mon"].apply(lambda x: 1 if x == 0 else x)
#     df["Ct_vs_Amt"] = df["Ct_vs_Amt"].apply(lambda x: "Dec_ct_inc_amt" if x == "Dec_ct_same_amt" else x)
#     df["Ct_vs_Amt"] = df["Ct_vs_Amt"].apply(lambda x: "Inc_ct_inc_amt" if x == "Same_ct_inc_amt" else x)
#     df["Contacts_Count_12_mon"] = df["Contacts_Count_12_mon"].apply(lambda x: 5 if x == 6 else x)
#     df["Card_&_Age"] = df["Card_&_Age"].apply(lambda x: "Rare" if df["Card_&_Age"].value_counts()[x] < 30 else x)
#
#     cat_cols, num_cols, cat_but_car = grab_col_names(df)
#
#     # Ordinal encoding:
#     categories_dict = {
#             "Education_Level": ['Uneducated', 'High School', 'College', 'Graduate', 'Post-Graduate', 'Doctorate', np.nan],
#             "Income_Category": ['Less than $40K', '$40K - $60K', '$60K - $80K', '$80K - $120K', '$120K +', np.nan],
#             "Customer_Age_Category": ['Young', 'Middle_Aged', 'Senior'],
#             "Card_Category": ['Blue', 'Silver', 'Gold_Platinum'],
#             "On_book_cat": ["<2_years", "<3_years", "<4_years", "<5_years"]}
#
#     def ordinal_encoder(dataframe, col):
#         if col in categories_dict:
#             col_cats = categories_dict[col]
#             ordinal_encoder = OrdinalEncoder(categories=[col_cats])
#             dataframe[col] = ordinal_encoder.fit_transform(dataframe[[col]])
#
#         return dataframe
#
#     for col in df.columns:
#         ordinal_encoder(df, col)
#
#     df.head()
#     cat_cols, num_cols, cat_but_car = grab_col_names(df)
#
#
#
#     df_ = one_hot_encoder(df, ["Gender"], drop_first=True)
#     df_.rename(columns={"Gender_M": "Gender"}, inplace=True)
#
#     # KNN Imputer
#     numeric_columns = df_.select_dtypes(include=['float64', 'int64']).columns
#     categorical_columns = [col for col in df_.columns if col not in numeric_columns]
#     df_numeric = df_[numeric_columns]
#     imputer = KNNImputer(n_neighbors=10)
#     df_numeric_imputed = pd.DataFrame(imputer.fit_transform(df_numeric), columns=numeric_columns)
#     df_concat = pd.concat([df_numeric_imputed, df[categorical_columns]], axis=1)
#     df_concat["Education_Level"] = df_concat["Education_Level"].round().astype('Int64')
#     df_concat["Income_Category"] = df_concat["Income_Category"].round().astype('Int64')
#     return df_concat[~outliers]

# Fonksiyonu kullanarak veri işleme
df = pd.read_csv("BankChurners.csv")
df = process_data(df)



#33333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333
#tüm görselleştirme

# Treemap
fig = px.treemap(df, path=['Target', 'Segment'], title="Target ve Segment")
fig.update_layout(height=600, width=800)
st.plotly_chart(fig)

#bubblechart
fig = px.scatter(
    df,
    x="Total_Amt_Chng_Q4_Q1",
    y="Avg_Utilization_Ratio",
    size="Important_client_score",
    color="Segment",
    hover_name="Customer_Age",
    size_max=60,
    title="Müşteri Değer Skorlarına Göre Bubble Chart"
)
st.plotly_chart(fig)



# Ürün sayısı arttıkça Churn olasılığı azalıyor
st.write("Ürün sayısı arttıkça Churn olasılığı azalıyor.")
mean_target_by_relationship = df.groupby("Total_Relationship_Count")["Target"].mean().reset_index()
fig = px.bar(mean_target_by_relationship, x="Total_Relationship_Count", y="Target",
             labels={"Total_Relationship_Count": "Toplam Ürün Sayısı", "Target": "Target"},
             title="Toplam Ürün Sayısına Göre Target", color_discrete_sequence=["blue"])
st.plotly_chart(fig)

# Yeni gelen müşteriler risk mi?
st.write("Yeni gelen müşteriler risk mi?")
mean_target_by_inactive_months = df.groupby("Months_Inactive_12_mon")["Target"].mean().reset_index()
fig = px.bar(mean_target_by_inactive_months, x="Months_Inactive_12_mon", y="Target",
             labels={"Months_Inactive_12_mon": "İnaktif Ay Sayısı", "Target": "Target"},
             title="İnaktif Ay Sayısına Göre Target", color_discrete_sequence=px.colors.qualitative.Pastel)
st.plotly_chart(fig)

# Borcu çok olanlar gidemiyor
mean_utilization_by_target = df.groupby("Target")["Avg_Utilization_Ratio"].mean().reset_index()
mean_revolving_bal_by_target = df.groupby("Target")["Total_Revolving_Bal"].mean().reset_index()
fig_utilization = px.bar(mean_utilization_by_target, x="Target", y="Avg_Utilization_Ratio",
                         labels={"Target": "Hedef", "Avg_Utilization_Ratio": "Borç/Kredi Limiti"},
                         title="Targete Göre Borç/Kredi Limiti", color_discrete_sequence=px.colors.qualitative.Pastel)
fig_utilization.update_layout(height=400, width=400)
fig_revolving_bal = px.bar(mean_revolving_bal_by_target, x="Target", y="Total_Revolving_Bal",
                           labels={"Target": "Hedef", "Total_Revolving_Bal": "Ortalama Devir Bakiyesi"},
                           title="Hedefe Göre Ortalama Devir Bakiyesi", color_discrete_sequence=px.colors.qualitative.Pastel)
fig_revolving_bal.update_layout(height=400, width=400)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_utilization)
with col2:
    st.plotly_chart(fig_revolving_bal)


# Gelir kategorilerine göre ortalama devir bakiyesi
fig = px.bar(df, x="Income_Category", y="Total_Revolving_Bal",
             labels={"Income_Category": "Gelir Kategorisi", "Total_Revolving_Bal": "Ortalama Devir Bakiyesi"},
             title="Gelir Kategorisine Göre Ortalama Devir Bakiyesi",
             color="Income_Category", color_discrete_sequence=px.colors.qualitative.Pastel)
# Grafiği görüntüle
st.plotly_chart(fig, use_container_width=True)

# Target'e göre Important_client_score'un grafiği:
mean_scores_by_target = df.groupby("Target")["Important_client_score"].mean().reset_index()
fig = px.bar(mean_scores_by_target, x="Target", y="Important_client_score",
             labels={"Target": "Hedef", "Important_client_score": "Ortalama Puan"},
             title="Targete Göre Important_client_score")
fig.update_layout(height=400, width=400)
st.plotly_chart(fig)

# müşteri ile iletişim sayısı ve target:
mean_churn_by_contact = df.groupby("Contacts_Count_12_mon")["Target"].mean().reset_index()
mean_churn_by_contact = mean_churn_by_contact.rename(columns={"Target": "Churn_Rate"})
fig = px.bar(mean_churn_by_contact, x="Contacts_Count_12_mon", y="Churn_Rate",
             labels={"Contacts_Count_12_mon": "İletişim Sayısı", "Churn_Rate": "Ortalama Churn Oranı"},
             title="İletişim Sayısına Göre Ortalama Churn Oranı")
fig.update_layout(height=400, width=400)
st.plotly_chart(fig)



#Age_&_Marital   Gender_&_Age        Card_&_Age değişkenlerini target ile baktım:
fig_age_marital = px.histogram(df, x="Age_&_Marital", color="Target", barmode="group",
                                labels={"Age_&_Marital": "Yaş ve Medeni Durum", "Target": "Churn Durumu"},
                                title="Yaş ve Medeni Duruma Göre Churn Durumu")
fig_age_marital.update_layout(xaxis_title="Yaş ve Medeni Durum", yaxis_title="Sayı")

fig_gender_age = px.histogram(df, x="Gender_&_Age", color="Target", barmode="group",
                               labels={"Gender_&_Age": "Cinsiyet ve Yaş", "Target": "Churn Durumu"},
                               title="Cinsiyet ve Yaşa Göre Churn Durumu")
fig_gender_age.update_layout(xaxis_title="Cinsiyet ve Yaş", yaxis_title="Sayı")

fig_card_age = px.histogram(df, x="Card_&_Age", color="Target", barmode="group",
                             labels={"Card_&_Age": "Kart ve Yaş", "Target": "Churn Durumu"},
                             title="Kart ve Yaşa Göre Churn Durumu")
fig_card_age.update_layout(xaxis_title="Kart ve Yaş", yaxis_title="Sayı")
st.plotly_chart(fig_age_marital)
st.plotly_chart(fig_gender_age)
st.plotly_chart(fig_card_age)


# burada Dec_ct_dec_amt kategorisi nedir? Çok fazla yoğunluk var orda
#  Ct_vs_Amt ile Target:
fig = px.histogram(df, x="Ct_vs_Amt", color="Target", barmode="group",
                   title="Ct_vs_Amt Değişkeninin Target İle İlişkisi",
                   labels={"Ct_vs_Amt": "Ct_vs_Amt", "Target": "Target Ortalaması"},
                   color_discrete_map={0: "lightblue", 1: "salmon"})

fig.update_layout(bargap=0.1)
st.plotly_chart(fig)

# bunun notunu almışım birlikte yorumlayalım.:
fig = px.scatter(df, x="Credit_Limit", y="Total_Revolving_Bal", color="Income_Category",
                 title="Kredi Limiti ve Devir Bakiyesi İlişkisi",
                 labels={"Credit_limit": "Kredi Limiti", "Total_revolving_Bal": "Devir Bakiyesi"},
                 color_discrete_sequence=px.colors.qualitative.Set2)
fig.update_layout(height=800, width=1200)
st.plotly_chart(fig)

#büyük Pasta
#'Education_Level' 'Income_Category' bunları da koycam Nanlar sorun çıkardı
fig = px.sunburst(df, path=['Target', 'Gender', 'Customer_Age_Category', 'Marital_Status'])
fig.update_layout(height=1000, width=1000)
# Streamlit ile gösterme
st.plotly_chart(fig)
#bunun farklı versiyonlarını deneyelim



# Gülen ve Somurtan Yüz Sembolleri
smile_image = "Pages/0.png"
frown_image = "Pages/11.png"
smile_count = 8500
frown_count = 1627
total_count = smile_count + frown_count
total_icons = 100
grid_size = 20
smile_icons = round(smile_count / total_count * total_icons)
frown_icons = total_icons - smile_icons
icons = [smile_image] * smile_icons + [frown_image] * frown_icons
for row in range(0, total_icons, grid_size):
    st.image(icons[row:row + grid_size], width=20, caption=None)






#personlar için grafik?
persona = ["May_marry", "Credit_builder_criteria","Family_criteria"]

grid = [st.columns(3) for _ in range(3)]
current_col = 0
row = 0

# Her bir feature için Target yüzdesini hesaplama ve grafik oluşturma
for feature in persona:
    if feature in df.columns:
        # Feature 1 olan kayıtları filtrele
        filtered_df = df[df[feature] == 1]

        # Target 1 olanların yüzdesini hesapla
        if not filtered_df.empty:
            percentage = (filtered_df['Target'].sum() / filtered_df.shape[0]) * 100
        else:
            percentage = 0  # Eğer feature 1 hiç yoksa

        # Yarım daire grafik oluştur
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=percentage,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"{feature}", 'font': {'size': 16}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "green"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, percentage], 'color': 'lavender'},
                    {'range': [percentage, 100], 'color': 'mintcream'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': percentage
                }
            }
        ))

        # Uygun sütunda Streamlit'te göster
        with grid[row][current_col]:
            st.plotly_chart(fig, use_container_width=True)

        current_col += 1
        if current_col > 2:
            current_col = 0
            row += 1



#




#½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½½
# Filtered DataFrames
filtered_df1 = df[df['Target'] == 1]
filtered_df0 = df[df['Target'] == 0]

# Kategorik değişkenler ve renkler
categories = ['Gender', 'Contacts_Count_12_mon', 'Total_Relationship_Count', 'Segment', 'Marital_Status']
colors = ['tab:blue', 'tab:green', 'tab:red', 'tab:pink', 'tab:orange']

# Figür oluştur, 2 subplot ile (1 row, 2 columns)
fig, axes = plt.subplots(1, 2, figsize=(10, 5), dpi=1000, subplot_kw={'projection': 'polar'})

# Target 1 için
ax = axes[0]
total_categories = sum(filtered_df1[cat].nunique() for cat in categories)
angles = np.linspace(0, 2 * np.pi, total_categories, endpoint=False)
bar_width = (2 * np.pi / total_categories) * 0.8  # %80 genişlik, %20 boşluk
start = 0
for i, category in enumerate(categories):
    unique_vals = df[category].unique()
    value_counts = filtered_df1[category].value_counts().reindex(unique_vals, fill_value=0)
    category_angles = angles[start:start + len(unique_vals)]
    bars = ax.bar(category_angles, value_counts, width=bar_width, color=colors[i], alpha=0.6, label=category, bottom=600)
    # Kategori değerlerinin isimlerini her barın üstüne yazma
    for bar, label in zip(bars, value_counts.index):
        angle = bar.get_x() + bar_width / 2  # Metni barın merkezine yerleştir
        height = 800
        ax.text(angle, height, str(label), color='black', ha='left', va='center', rotation=np.degrees(angle),
                rotation_mode='anchor', fontsize=7)
    start += len(unique_vals)
    ax.text(0, 0, "1", color='black', ha='center', va='center', fontsize=12)
fig.legend()
# Target 0 için
ax = axes[1]
total_categories = sum(filtered_df0[cat].nunique() for cat in categories)
angles = np.linspace(0, 2 * np.pi, total_categories, endpoint=False)
start = 0
for i, category in enumerate(categories):
    unique_vals = df[category].unique()
    value_counts = filtered_df0[category].value_counts().reindex(unique_vals, fill_value=0)
    category_angles = angles[start:start + len(unique_vals)]
    bars = ax.bar(category_angles, value_counts, width=bar_width, color=colors[i], alpha=0.6, label=category, bottom=3000)
    # Kategori değerlerinin isimlerini her barın üstüne yazma
    for bar, label in zip(bars, value_counts.index):
        angle = bar.get_x() + bar_width / 2  # Metni barın merkezine yerleştir
        height = 3800
        ax.text(angle, height, str(label), color='black', ha='left', va='center', rotation=np.degrees(angle),
                rotation_mode='anchor', fontsize=7)
    start += len(unique_vals)
    ax.text(0, 0, "0", color='black', ha='center', va='center', fontsize=12)

# Ortak ayarlar
for ax in axes:
    ax.grid(False)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.spines['polar'].set_visible(False)

# Streamlit'te göster
st.pyplot(fig)
















# PCA ve waffle plot:
#bunu yapabilmek için tüm veri scale edilmiş olmalı
#o yüzden modele kadar herşeyi üste ekledim























progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()
last_rows = np.random.randn(1, 1)
chart = st.line_chart(last_rows)

for i in range(1, 101):
    new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
    status_text.text("%i%% Complete" % i)
    chart.add_rows(new_rows)
    progress_bar.progress(i)
    last_rows = new_rows
    time.sleep(0.05)

progress_bar.empty()

# Streamlit widgets automatically run the script from top to bottom. Since
# this button is not connected to any other logic, it just causes a plain
# rerun.
st.button("Re-run")


######## DİLARA RADAR BAŞLANGIÇ

# Libraries
import matplotlib.pyplot as plt
import pandas as pd
from math import pi

df.head()

# ------- PART 0: Reverse MinMax Scaler
df0 = pd.read_csv("BankChurners.csv")
df[['Total_Trans_Ct', 'Total_Trans_Amt']] = df0[['Total_Trans_Ct', 'Total_Trans_Amt']]
df["Days_Inactive_Last_Year"] = df0["Months_Inactive_12_mon"] * 30
df["Days_Inactive_Last_Year"].replace(0, 30, inplace=True)
df["Days_Inactive_Last_Year"].replace(180, 150, inplace=True)

# Set data
df_radar = pd.DataFrame({
    'group': ['Hibernating', 'At Risk', "Can't Lose", 'About to Sleep', 'Need Attention', 'Loyal Customers', 'Promising', 'New Customers', 'Potential Loyalists', 'Champions'],
    'Total_Trans_Amt': [df[df["Segment"]=='Hibernating']["Total_Trans_Amt"].mean(), df[df["Segment"]=="At Risk"]["Total_Trans_Amt"].mean(), df[df["Segment"]=="Can't Lose"]["Total_Trans_Amt"].mean(), df[df["Segment"]=='About to Sleep']["Total_Trans_Amt"].mean(), df[df["Segment"]=='Need Attention']["Total_Trans_Amt"].mean(), df[df["Segment"]=='Loyal Customers']["Total_Trans_Amt"].mean(), df[df["Segment"]=='Promising']["Total_Trans_Amt"].mean(), df[df["Segment"]=='New Customers']["Total_Trans_Amt"].mean(), df[df["Segment"]=='Potential Loyalists']["Total_Trans_Amt"].mean(), df[df["Segment"]=="Champions"]["Total_Trans_Amt"].mean()],
    'Total_Trans_Ct': [df[df["Segment"]=="Hibernating"]["Total_Trans_Ct"].mean(), df[df["Segment"]=="At Risk"]["Total_Trans_Ct"].mean(), df[df["Segment"]=="Can't Lose"]["Total_Trans_Ct"].mean(), df[df["Segment"]=='About to Sleep']["Total_Trans_Ct"].mean(), df[df["Segment"]=='Need Attention']["Total_Trans_Ct"].mean(), df[df["Segment"]=='Loyal Customers']["Total_Trans_Ct"].mean(), df[df["Segment"]=='Promising']["Total_Trans_Ct"].mean(), df[df["Segment"]=='New Customers']["Total_Trans_Ct"].mean(), df[df["Segment"]=='Potential Loyalists']["Total_Trans_Ct"].mean(), df[df["Segment"]=="Champions"]["Total_Trans_Ct"].mean()],
    'Important_client_score': [df[df["Segment"]=="Hibernating"]["Important_client_score"].mean(), df[df["Segment"]=="At Risk"]["Important_client_score"].mean(), df[df["Segment"]=="Can't Lose"]["Important_client_score"].mean(), df[df["Segment"]=='About to Sleep']["Important_client_score"].mean(), df[df["Segment"]=='Need Attention']["Important_client_score"].mean(), df[df["Segment"]=='Loyal Customers']["Important_client_score"].mean(), df[df["Segment"]=='Promising']["Important_client_score"].mean(), df[df["Segment"]=='New Customers']["Important_client_score"].mean(), df[df["Segment"]=='Potential Loyalists']["Important_client_score"].mean(), df[df["Segment"]=="Champions"]["Important_client_score"].mean()],
    'Days_Inactive_Last_Year': [df[df["Segment"]=="Hibernating"]["Days_Inactive_Last_Year"].mean(), df[df["Segment"]=="At Risk"]["Days_Inactive_Last_Year"].mean(), df[df["Segment"]=="Can't Lose"]["Days_Inactive_Last_Year"].mean(), df[df["Segment"]=='About to Sleep']["Days_Inactive_Last_Year"].mean(), df[df["Segment"]=='Need Attention']["Days_Inactive_Last_Year"].mean(), df[df["Segment"]=='Loyal Customers']["Days_Inactive_Last_Year"].mean(), df[df["Segment"]=='Promising']["Days_Inactive_Last_Year"].mean(), df[df["Segment"]=='New Customers']["Days_Inactive_Last_Year"].mean(), df[df["Segment"]=='Potential Loyalists']["Days_Inactive_Last_Year"].mean(), df[df["Segment"]=="Champions"]["Days_Inactive_Last_Year"].mean()],
    'Total_Relationship_Count': [df[df["Segment"]=="Hibernating"]["Total_Relationship_Count"].mean(), df[df["Segment"]=="At Risk"]["Total_Relationship_Count"].mean(), df[df["Segment"]=="Can't Lose"]["Total_Relationship_Count"].mean(), df[df["Segment"]=='About to Sleep']["Total_Relationship_Count"].mean(), df[df["Segment"]=='Need Attention']["Total_Relationship_Count"].mean(), df[df["Segment"]=='Loyal Customers']["Total_Relationship_Count"].mean(), df[df["Segment"]=='Promising']["Total_Relationship_Count"].mean(), df[df["Segment"]=='New Customers']["Total_Relationship_Count"].mean(), df[df["Segment"]=='Potential Loyalists']["Total_Relationship_Count"].mean(), df[df["Segment"]=="Champions"]["Total_Relationship_Count"].mean()]
})

# ------- PART 1: Create background
# number of variable
categories = list(df_radar)[1:]
N = len(categories)

# What will be the angle of each axis in the plot? (we divide the plot / number of variable)
angles = [n / float(N) * 2 * pi for n in range(N)]
angles += angles[:1]

# Initialise the spider plot
ax = plt.subplot(111, polar=True)

# If you want the first axis to be on top:
ax.set_theta_offset(pi / 2)
ax.set_theta_direction(-1)

# Draw one axe per variable + add labels
plt.xticks(angles[:-1], categories)

# Draw ylabels
ax.set_rlabel_position(0)
plt.yticks([2, 4, 6, 8], ["2", "4", "6", "8"], color="grey", size=7)
plt.ylim(0, 10)

# ------- PART 2: Add plots

# Plot each individual = each line of the data
# I don't make a loop, because plotting more than 3 groups makes the chart unreadable

# Ind1
values = df_radar.loc[0].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="Hibernating")
ax.fill(angles, values, 'b', alpha=0.1)

# Ind2
values = df_radar.loc[1].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="At Risk")
ax.fill(angles, values, 'r', alpha=0.1)

# Ind3
values = df_radar.loc[2].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="Can't Lose")
ax.fill(angles, values, '#ff7f0e', alpha=0.1)

# Ind4
values = df_radar.loc[3].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label='About to Sleep')
ax.fill(angles, values, '#2ca02c', alpha=0.1)

# Ind5
values = df_radar.loc[4].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label='Need Attention')
ax.fill(angles, values, '#9467bd', alpha=0.1)

# Ind6
values = df_radar.loc[5].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label='Loyal Customers')
ax.fill(angles, values, '#8c564b', alpha=0.1)

# Ind7
values = df_radar.loc[6].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="Promising")
ax.fill(angles, values, '#e377c2', alpha=0.1)

# Ind8
values = df_radar.loc[7].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="New Customers")
ax.fill(angles, values, '#7f7f7f', alpha=0.1)

# Ind9
values = df_radar.loc[8].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="Potential Loyalists")
ax.fill(angles, values, '#bcbd22', alpha=0.1)

# Ind10
values = df_radar.loc[9].drop('group').values.flatten().tolist()
values += values[:1]
ax.plot(angles, values, linewidth=1, linestyle='solid', label="Champions")
ax.fill(angles, values, '#17becf', alpha=0.1)

# Add legend
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

# Show the graph
plt.show()


######## DİLARA RADAR BİTİŞ