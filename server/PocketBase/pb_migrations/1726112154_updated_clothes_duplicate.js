/// <reference path="../pb_data/types.d.ts" />
migrate((db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("ich8v3chir4a2bo")

  collection.name = "clothes"
  collection.indexes = [
    "CREATE UNIQUE INDEX `idx_HT3S6yl` ON `clothes` (`product_url`)",
    "CREATE UNIQUE INDEX `idx_DVOTByW` ON `clothes` (`image_url`)"
  ]

  return dao.saveCollection(collection)
}, (db) => {
  const dao = new Dao(db)
  const collection = dao.findCollectionByNameOrId("ich8v3chir4a2bo")

  collection.name = "clothes_duplicate"
  collection.indexes = [
    "CREATE UNIQUE INDEX `idx_HT3S6yl` ON `clothes_duplicate` (`product_url`)",
    "CREATE UNIQUE INDEX `idx_DVOTByW` ON `clothes_duplicate` (`image_url`)"
  ]

  return dao.saveCollection(collection)
})
