/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("5ic961ua5961svk")

  collection.name = "clothes"
  collection.indexes = [
    "CREATE UNIQUE INDEX `idx_rGxINUn` ON `clothes` (`product_url`)"
  ]

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("5ic961ua5961svk")

  collection.name = "clothes_duplicate"
  collection.indexes = [
    "CREATE UNIQUE INDEX `idx_rGxINUn` ON `clothes_duplicate` (`product_url`)"
  ]

  return dao.saveCollection(collection)
})
