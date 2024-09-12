/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("bbtugrjvh722hx5")

  collection.name = "clothes"
  collection.indexes = [
    "CREATE UNIQUE INDEX `idx_7OsNLad` ON `clothes` (`product_url`)"
  ]

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("bbtugrjvh722hx5")

  collection.name = "clothes_duplicate"
  collection.indexes = [
    "CREATE UNIQUE INDEX `idx_7OsNLad` ON `clothes_duplicate` (`product_url`)"
  ]

  return dao.saveCollection(collection)
})
