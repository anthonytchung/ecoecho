/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("s7pul2oc2iixnly")

  collection.name = "clothes"
  collection.indexes = [
    "CREATE UNIQUE INDEX `idx_CIDkXMd` ON `clothes` (`product_url`)",
    "CREATE UNIQUE INDEX `idx_gzJxoqD` ON `clothes` (`image_url`)"
  ]

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("s7pul2oc2iixnly")

  collection.name = "clothes_duplicate"
  collection.indexes = [
    "CREATE UNIQUE INDEX `idx_CIDkXMd` ON `clothes_duplicate` (`product_url`)",
    "CREATE UNIQUE INDEX `idx_gzJxoqD` ON `clothes_duplicate` (`image_url`)"
  ]

  return dao.saveCollection(collection)
})
