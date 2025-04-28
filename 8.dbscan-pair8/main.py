from fastapi import FastAPI
from ProductClustering import df as product_df
from SupplierClustering import df as supplier_df
from CountryClustering import df as country_df
from Database import engine

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "DBSCAN API is up and running"}

@app.get("/cluster/products")
def cluster_products():
    return {
        "clusters": product_df["cluster"].tolist(),
        "products": product_df["product_id"].tolist()
    }

@app.get("/cluster/suppliers")
def cluster_suppliers():
    return {
        "clusters": supplier_df["cluster"].tolist(),
        "suppliers": supplier_df["supplier_id"].tolist()
    }

@app.get("/cluster/countries")
def cluster_countries():
    return {
        "clusters": country_df["cluster"].tolist(),
        "countries": country_df["country"].tolist()
    }
