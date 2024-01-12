=====================
**Mrp Customization**
=====================

**Description**
***************
* Technical name: mrp_customization
* This module is used to create child manufaturing orders based on the field "Max Quantity"(max_qty) on Bill of materials

**Author**
**********
* BizzAppDev Systems PVT. LTD.

**Used by**
***********
* #N/A

**Installation**
****************
* Install from the standard modules in the app store.

**Configuration**
*****************
* In Bill of Materials "Max Quantity" should be set.

**Usage**
*********
* #T7141 - MAD:
    - When the value of "Max Quantity"(max_qty) is set then on pressing button "Split MO" the current MO will be cancled and its child MO will be created based on "Max Quantity"(max_qty) on BoM level and "Quantity"(product_qty) on MO level.

**Known issues/Roadmap**
************************
* #N/A

**Changelog**
*************
* 02-01-2024 - T7141 - MAD - Child Prodution Orders
