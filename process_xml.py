import os
import json
import logging
import xml.etree.ElementTree as ET

# Set up logging
logging.basicConfig(
    filename='process.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define the path to the XML files
xml_folder = 'C:/Users/nandu/OneDrive/Documents/H2N-DEV-interview/main/'

def parse_order(order_element, file_path):
    """Parse individual order element and return a JSON object."""
    try:
        order_data = {}
        order_data['OrderID'] = order_element.find('OrderID').text if order_element.find('OrderID') is not None else None
        
        customer = order_element.find('Customer')
        if customer is not None:
            order_data['Customer'] = {
                'CustomerID': customer.find('CustomerID').text if customer.find('CustomerID') is not None else None,
                'Name': customer.find('Name').text if customer.find('Name') is not None else None,
            }
        else:
            logging.warning(f'Skipped {os.path.basename(file_path)} - Missing <Customer> element.')
            return None

        # Extract products
        products = []
        products_element = order_element.find('Products')
        if products_element is not None:
            for product in products_element.findall('Product'):
                product_data = {
                    'ProductID': product.find('ProductID').text if product.find('ProductID') is not None else None,
                    'Name': product.find('Name').text if product.find('Name') is not None else None,
                    'Quantity': product.find('Quantity').text if product.find('Quantity') is not None else None,
                    'Price': product.find('Price').text if product.find('Price') is not None else None
                }
                products.append(product_data)
        else:
            logging.warning(f'Skipped {os.path.basename(file_path)} - Missing <Products> element.')
            return None
        order_data['Products'] = products



        # Check for unexpected fields
        expected_fields = {'OrderID', 'Customer', 'OrderDate', 'Products', 'TotalAmount'}
        unexpected_fields = set(order_element.keys()) - expected_fields
        
        for child in order_element:
            if child.tag not in expected_fields:
                unexpected_fields.add(child.tag)

        if unexpected_fields:
            logging.warning(f'Warning in {os.path.basename(file_path)} - Unexpected field(s) {", ".join(unexpected_fields)}.')

        return order_data

    except Exception as e:
        logging.error(f'Error processing order in {os.path.basename(file_path)}: {str(e)}')
        return None


def parse_xml_to_json(file_path):
    """Parse XML file and convert it to JSON, handling both single and multiple order formats."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # List to store parsed order data
        orders_data = []

        # Handle both single-order and multi-order XML files
        if root.tag == 'Order':  # Single order
            order_data = parse_order(root, file_path)
            if order_data:
                orders_data.append(order_data)
        elif root.tag == 'Orders':  # Multiple orders
            for order in root.findall('Order'):
                order_data = parse_order(order, file_path)
                if order_data:
                    orders_data.append(order_data)
        else:
            logging.warning(f'Skipped {os.path.basename(file_path)} - Invalid root element <{root.tag}>.')

        if orders_data:
            return json.dumps(orders_data, indent=4)

    except ET.ParseError as e:
        logging.error(f'Parsing error in {os.path.basename(file_path)} - {str(e)}.')
    except Exception as e:
        logging.error(f'Error processing {os.path.basename(file_path)}: {str(e)}')

    return None

def main():
    """Main function to iterate through XML files and process them."""
    json_data_list = []

    for filename in os.listdir(xml_folder):
        if filename.endswith('.xml'):
            file_path = os.path.join(xml_folder, filename)
            json_data = parse_xml_to_json(file_path)
            if json_data is not None:
                json_data_list.append(json_data)

    # Save the JSON data to a file
    with open('output.json', 'w') as json_file:
        json.dump(json_data_list, json_file, indent=4)

if __name__ == '__main__':
    main()
