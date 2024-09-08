/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("apxn976fd4a0p7k")

  collection.indexes = [
    "CREATE INDEX `idx_5agg5am` ON `clothes` (`product_url`)"
  ]

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("apxn976fd4a0p7k")

  collection.indexes = []

  return dao.saveCollection(collection)
})
