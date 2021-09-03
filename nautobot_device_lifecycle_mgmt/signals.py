"""Custom signals for the LifeCycle Management plugin."""

from nautobot.extras.choices import RelationshipTypeChoices


def post_migrate_create_relationships(sender, apps, **kwargs):  # pylint: disable=unused-argument
    """Callback function for post_migrate() -- create Relationship records."""
    # pylint: disable=invalid-name
    SoftwareLCM = sender.get_model("SoftwareLCM")
    ContentType = apps.get_model("contenttypes", "ContentType")
    _Device = apps.get_model("dcim", "Device")
    InventoryItem = apps.get_model("dcim", "InventoryItem")
    Relationship = apps.get_model("extras", "Relationship")

    contract_lcm = sender.get_model("ContractLCM")

    for relationship_dict in [
        {
            "name": "Software on Device",
            "slug": "device_soft",
            "type": RelationshipTypeChoices.TYPE_ONE_TO_MANY,
            "source_type": ContentType.objects.get_for_model(SoftwareLCM),
            "source_label": "Running on Devices",
            "destination_type": ContentType.objects.get_for_model(_Device),
            "destination_label": "Software Version",
        },
        {
            "name": "Software on InventoryItem",
            "slug": "inventory_item_soft",
            "type": RelationshipTypeChoices.TYPE_ONE_TO_MANY,
            "source_type": ContentType.objects.get_for_model(SoftwareLCM),
            "source_label": "Running on Inventory Items",
            "destination_type": ContentType.objects.get_for_model(InventoryItem),
            "destination_label": "Software Version",
        },
        {
            "name": "Contract to dcim.Device",
            "slug": "contractlcm-to-device",
            "type": RelationshipTypeChoices.TYPE_MANY_TO_MANY,
            "source_type": ContentType.objects.get_for_model(contract_lcm),
            "source_label": "Devices",
            "destination_type": ContentType.objects.get_for_model(_Device),
            "destination_label": "Contracts",
        },
        {
            "name": "Contract to dcim.InventoryItem",
            "slug": "contractlcm-to-inventoryitem",
            "type": RelationshipTypeChoices.TYPE_ONE_TO_MANY,
            "source_type": ContentType.objects.get_for_model(contract_lcm),
            "source_label": "Inventory Items",
            "destination_type": ContentType.objects.get_for_model(InventoryItem),
            "destination_label": "Contract",
        },
    ]:
        Relationship.objects.get_or_create(name=relationship_dict["name"], defaults=relationship_dict)
