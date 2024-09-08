/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("ijmnikg30ryqxfl")

  collection.indexes = [
    "CREATE UNIQUE INDEX `idx_LAGEhKF` ON `clothes` (`product_url`)"
  ]

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("ijmnikg30ryqxfl")

  collection.indexes = []

  return dao.saveCollection(collection)
})
