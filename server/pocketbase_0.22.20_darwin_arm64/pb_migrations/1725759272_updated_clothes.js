/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("ijmnikg30ryqxfl")

  // remove
  collection.schema.removeField("vjphqj7w")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "rmtcjwra",
    "name": "features",
    "type": "text",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "pattern": ""
    }
  }))

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("ijmnikg30ryqxfl")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "vjphqj7w",
    "name": "features",
    "type": "number",
    "required": false,
    "presentable": false,
    "unique": false,
    "options": {
      "min": null,
      "max": null,
      "noDecimal": false
    }
  }))

  // remove
  collection.schema.removeField("rmtcjwra")

  return dao.saveCollection(collection)
})
