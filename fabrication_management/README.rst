functional flow for Fabrication_management:
    - 1st create sale-order(smart button: PO, Project, Tasks)
        - add custom fields for type of welding and type of steel
        - cron to send email every 2 months about miantanence(after invoice generation)
    - based on sale order we create purchase order
        - run cron to replenish stock based on avilable stock and sale orders
    - based on sale order we create project & task
    - Demo data with products and partners
