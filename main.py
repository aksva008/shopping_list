import flet as ft


def main(page: ft.Page):
    page.title = "Список покупок"
    page.theme_mode = ft.ThemeMode.LIGHT

    products = []
    filter_type = "all"

    product_list = ft.Column(spacing=10)
    counter_text = ft.Text("Куплено: 0")


    def update_counter():
        bought = sum(1 for p in products if p["checkbox"].value)
        counter_text.value = f"Куплено: {bought}"
        page.update()

    def load_products():
        product_list.controls.clear()

        for product in products:
            bought = product["checkbox"].value

            if filter_type == "all":
                product_list.controls.append(product["row"])
            elif filter_type == "bought" and bought:
                product_list.controls.append(product["row"])
            elif filter_type == "not_bought" and not bought:
                product_list.controls.append(product["row"])

        update_counter()
        page.update()

    def toggle_product(_):
        load_products()

    def delete_product(product):
        products.remove(product)
        load_products()

    def create_product_row(name, count):
        checkbox = ft.Checkbox(
            label=f"{name} (x{count})",
            on_change=toggle_product
        )

        product = {}

        delete_button = ft.IconButton(
            icon=ft.icons.DELETE,
            on_click=lambda e: delete_product(product)
        )

        row = ft.Row(
            controls=[checkbox, delete_button],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        product["checkbox"] = checkbox
        product["row"] = row

        return product

    def add_product(_):
        if product_input.value:
            product = create_product_row(
                product_input.value,
                count_input.value
            )
            products.append(product)

            product_input.value = ""
            count_input.value = "1"

            load_products()

    def set_filter(value):
        nonlocal filter_type
        filter_type = value
        load_products()


    product_input = ft.TextField(
        label="Товар",
        expand=True,
        on_submit=add_product
    )

    count_input = ft.TextField(
        label="Сколько",
        width=100,
        value="1"
    )

    add_button = ft.ElevatedButton("ADD", on_click=add_product)

    filter_buttons = ft.Row(
        [
            ft.ElevatedButton("Все", on_click=lambda e: set_filter("all")),
            ft.ElevatedButton("Купленные", on_click=lambda e: set_filter("bought")),
            ft.ElevatedButton("Некупленные", on_click=lambda e: set_filter("not_bought")),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY
    )

    page.add(
        ft.Text("Список покупок", size=24, weight="bold"),
        ft.Row([product_input, count_input, add_button]),
        filter_buttons,
        counter_text,
        product_list
    )


ft.app(target=main)

