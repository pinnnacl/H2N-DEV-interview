import os
import json
import logging
import xml.etree.ElementTree as ET
from datetime import datetime

# Set up logging
logging.basicConfig(
    filename='process.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define the path to the XML files
xml_folder = 'C:/Users/nandu/OneDrive/Documents/H2N-DEV-interview/base/'


def parse_xml_to_json(file_path):
    """Parse XML file and convert to JSON."""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Extract key fields
        order_data = {}
        order_data['OrderID'] = root.find('OrderID').text if root.find('OrderID') is not None else None
        customer = root.find('Customer')
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
        products_element = root.find('Products')
        if products_element is not None:
            for product in products_element.findall('Product'):
                product_data = {
                    'ProductID': product.find('ProductID').text if product.find('ProductID') is not None else None,
                    'Name': product.find('Name').text if product.find('Name') is not None else None,
                    'Quantity': product.find('Quantity').text if product.find('Quantity') is not None else None,
                    'Price': product.find('Price').text if product.find('Price') is not None else None
                }
                products.append(product_data)
        order_data['Products'] = products

        # Check for unexpected fields
        expected_fields = {'OrderID', 'Customer', 'OrderDate', 'Products', 'TotalAmount'}
        unexpected_fields = set(root.keys()) - expected_fields
        
        # Check for unexpected children of the root
        for child in root:
            if child.tag not in expected_fields:
                unexpected_fields.add(child.tag)

        # Log unexpected fields if any
        if unexpected_fields:
            logging.warning(f'Warning in {os.path.basename(file_path)} - Unexpected field(s) {", ".join(unexpected_fields)}.')

        # Return order data as JSON
        return json.dumps(order_data)

    except ET.ParseError:
        logging.error(f'Parsing error in {os.path.basename(file_path)} - Malformed XML.')
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

if __name__ == '__main__':
    main()
