TASK_TYPE = "shopping"

TASK_SCHEMA = {
    "shopping": [
        ["you are on the search results page and candidate products are shown", "you have not selected a product yet", "select the most relevant product from the list based on the instruction and keywords"],
        ["every product on the current page has been clicked or is above the price limit", "you have not found the target product yet", "click Next > to view more products"],
        ["you are on a single product detail page", "you have not selected any product option yet", "click Description to view the product details"],
        ["you are on a product detail page that has options", "you have selected a product and its matching options are not all clicked", "click the option that matches the instruction and keywords"],
        ["you are on a product detail page", "you have selected a product and all matching options are clicked or there are no options", "click Buy Now"],
        ["the selected product does not match the instruction or lacks a required option", "you have selected a product", "click < Prev to return to the search results"],
        ["you are on a Description, Features, or Reviews sub-page", "you have not selected a product yet", "click < Prev to return to the product detail page"],
    ]
}

def get_schema(task_type):
    return TASK_SCHEMA[task_type]
