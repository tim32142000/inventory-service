import os

import requests
import streamlit as st

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
)

CATEGORIES = [
    "food",
    "drink",
    "book",
    "others",
]


def get_api_error_message(
    response: requests.Response,
    default_message: str,
) -> str:
    fallback = f"{default_message} (HTTP {response.status_code})"

    try:
        error_data = response.json()
    except requests.exceptions.JSONDecodeError:
        return fallback

    if isinstance(error_data, dict):
        return str(error_data.get("detail") or fallback)

    return fallback


st.title("Inventory Service")

if "success_message" in st.session_state:
    st.success(st.session_state.pop("success_message"))

st.subheader("商品列表")

category_filter = st.selectbox("篩選類別", ["all"] + CATEGORIES)

params = {}

if category_filter != "all":
    params["category"] = category_filter


try:
    response = requests.get(f"{API_BASE_URL}/items", params=params, timeout=10)
except requests.RequestException:
    st.error("無法連接 Inventory API，請確認 FastAPI 是否已啟動。")
    st.stop()

if not response.ok:
    st.error(get_api_error_message(response, "載入商品失敗"))
    st.stop()

items = response.json()
st.dataframe(items)

st.subheader("新增商品")

with st.form("create_item_form"):
    name = st.text_input("商品名稱")
    category = st.selectbox("商品類別", CATEGORIES)
    price = st.number_input("價格", min_value=0, step=1)
    quantity = st.number_input("數量", min_value=0, step=1)

    submitted = st.form_submit_button("新增商品")

if submitted:
    new_item = {
        "name": name,
        "category": category,
        "price": price,
        "quantity": quantity,
    }

    try:
        create_response = requests.post(
            f"{API_BASE_URL}/items", json=new_item, timeout=10
        )

    except requests.RequestException:
        st.error("無法連接 Inventory API，新增失敗。")

    else:
        if create_response.status_code == 201:
            created_item = create_response.json()

            st.session_state["success_message"] = f"新增成功：{created_item['name']}"
            st.rerun()

        else:
            st.error(
                get_api_error_message(
                    create_response,
                    "新增失敗",
                )
            )

st.subheader("更新商品")

with st.container(border=True):

    if items:
        selected_update_item = st.selectbox(
            "選擇要更新的商品",
            items,
            format_func=lambda item: f"{item['name']} (ID: {item['id']})",
            key="selected_update_item",
        )

        current_category = selected_update_item["category"]

        if current_category in CATEGORIES:
            category_index = CATEGORIES.index(current_category)
        else:
            category_index = CATEGORIES.index("others")

        item_id = selected_update_item["id"]

        with st.form("update_item_form"):
            updated_name = st.text_input(
                "商品名稱",
                value=selected_update_item["name"],
                key=f"update_name_{item_id}",
            )

            updated_category = st.selectbox(
                "商品類別",
                CATEGORIES,
                index=category_index,
                key=f"update_category_{item_id}",
            )

            updated_price = st.number_input(
                "價格",
                min_value=0,
                value=selected_update_item["price"],
                step=1,
                key=f"update_price_{item_id}",
            )

            updated_quantity = st.number_input(
                "數量",
                min_value=0,
                value=selected_update_item["quantity"],
                step=1,
                key=f"update_quantity_{item_id}",
            )

            updated_submitted = st.form_submit_button("更新商品")

        if updated_submitted:
            updated_item = {
                "name": updated_name,
                "category": updated_category,
                "price": updated_price,
                "quantity": updated_quantity,
            }

            try:
                update_response = requests.put(
                    f"{API_BASE_URL}/items/{item_id}",
                    json=updated_item,
                    timeout=10,
                )

            except requests.RequestException:
                st.error("無法連接 Inventory API，更新失敗。")

            else:
                if update_response.ok:
                    updated_item_response = update_response.json()

                    st.session_state["success_message"] = (
                        f"更新成功：{updated_item_response['name']} (ID: {item_id})"
                    )

                    st.rerun()

                else:
                    st.error(
                        get_api_error_message(
                            update_response,
                            "更新失敗",
                        )
                    )

    else:
        st.info("目前列表中沒有可更新的商品")

st.subheader("刪除商品")

with st.container(border=True):

    if items:

        selected_item = st.selectbox(
            "選擇要刪除的商品",
            items,
            format_func=lambda item: f"{item['name']} (ID: {item['id']})",
        )

        delete_clicked = st.button("刪除商品")

        if delete_clicked:
            try:
                delete_response = requests.delete(
                    f"{API_BASE_URL}/items/{selected_item['id']}", timeout=10
                )

            except requests.RequestException:
                st.error("無法連接 Inventory API，刪除失敗。")

            else:
                if delete_response.ok:
                    st.session_state["success_message"] = (
                        f"刪除成功：{selected_item['name']} (ID: {selected_item['id']})"
                    )
                    st.rerun()
                else:
                    st.error(
                        get_api_error_message(
                            delete_response,
                            "刪除失敗",
                        )
                    )

    else:
        st.info("目前列表中沒有可刪除的商品")
