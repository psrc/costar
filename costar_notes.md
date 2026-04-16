#### Instructions for exporting data from Costar
 - Filter geography by going to Filters -> Location -> Market
    - Add Seattle and Bremerton
 - Filter for supermarkets by going to Filters -> Building
    - Select "Supermarkets" or "Hospitals" from "Secondary Type" drop down
 - Make sure you are zoomed out far enough to see entire region and click "export" in top right
 - Select "lat/long" from the "Selected Field Layout"
    - if "lat/long" is not a saved template in your Costar account you can easily recreate it by adding "latitude", "longitude" and "anchor tenants". Make sure and save it and name it "lat/long" for reuse in future exports.

 - You will need to do some additional exports to download grocery stores that aren't  categorized as supermarkets
    - Go to Filters -> Tenants 
        - Search for a grocery store by name ie. Walmart Neighborhood Market" in the "Properties containing (tenant or store type)"


#### Initial notes of data:
 - 111 out of 268 Supermarkets don't have a property name - might need to double check those
 - Already had to add walmart,walmart neighborhood market and costco in manually by searching for their names in the 'tenants" filter in costar since they are not categorized as supermarkets, there is likely more stores that are not categorized correctly and it would take time to find them all and add them
 - I'm hesitant to do an extensive data clean up since the source data it self wouldn't be cleaned - future downloads of this data would have to be reconciled with our cleaned version for changes and that could be very complicated to do