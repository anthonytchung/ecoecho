/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("ijmnikg30ryqxfl")

  // add
  collection.schema.addField(new SchemaField({
    "system": false,
    "id": "wgiewsgu",
    "name": "available_sizes",
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

  // remove
  collection.schema.removeField("wgiewsgu")

  return dao.saveCollection(collection)
})
