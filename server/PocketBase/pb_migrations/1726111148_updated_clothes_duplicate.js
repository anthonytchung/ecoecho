/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("jaml5sjph8qr69p")

  collection.name = "clothes"
  collection.indexes = [
    "CREATE UNIQUE INDEX `idx_7JPJcQg` ON `clothes` (`product_url`)"
  ]

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("jaml5sjph8qr69p")

  collection.name = "clothes_duplicate"
  collection.indexes = [
    "CREATE UNIQUE INDEX `idx_7JPJcQg` ON `clothes_duplicate` (`product_url`)"
  ]

  return dao.saveCollection(collection)
})
