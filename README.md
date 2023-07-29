# Real Estate Module for Odoo

## Description

This is a custom Odoo module for managing real estate properties and offers. It allows users to create, view, and manage properties along with associated offers from potential buyers.

## Features

- Create and manage real estate properties with details such as name, description, bedrooms, living area, garden, etc.
- Track the state of properties (New, Offer Received, Offer Accepted, Sold, Canceled).
- Add and manage property offers with details like price, partner, and status.
- Compute total area and best offer automatically based on property details and offers.
- Provide a default value for garden area and orientation when the garden field is set.
- Prevent users from entering incorrect data using SQL constraints and Python constraints.

## Odoo Version

This module has been developed and tested on Odoo version 14.

## Installation

1. Clone this repository to your Odoo addons directory.
2. Restart your Odoo server.
3. Go to the Odoo Apps menu and click on the "Update Apps List" button.
4. Search for "Real Estate" module and click on the "Install" button.
5. After installation, the "Real Estate Properties" menu will appear in the Odoo dashboard.

## Requirements

No additional Python packages are required for this module.

## Usage

1. Go to the "Real Estate Properties" menu to manage properties and offers.
2. Create a new property by clicking on the "Create" button and fill in the necessary details.
3. Add offers to a property by going to the "Offers" tab and clicking on "Add an Item".
4. Set the property state to "Offer Accepted" to mark the property as sold.
