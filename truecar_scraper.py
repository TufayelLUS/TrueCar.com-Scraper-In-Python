import requests
import json
import csv
import os
import base64


# Get webscraping softwares like this on fiverr: https://www.fiverr.com/thechoyon

output_file_name = 'used_car_data.csv'  # set output file name


class TrueCar():
    def __init__(self):
        self.api_url = "https://www.truecar.com/abp/api/graphql/"

    def saveData(self, dataset):
        with open(output_file_name, mode='a+', encoding='utf-8-sig', newline='') as csvFile:
            fieldnames = ["Car Company", "Car Model", "Style Name", "Year",
                          "Mileage", "Transmission Type", "Engine", "Fuel Type", "Body Type", "Price", "Link"]
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            if os.stat(output_file_name).st_size == 0:
                writer.writeheader()
            writer.writerow({
                "Car Company": dataset[0],
                "Car Model": dataset[1],
                "Style Name": dataset[2],
                "Year": dataset[3],
                "Mileage": dataset[4],
                "Transmission Type": dataset[5],
                "Engine": dataset[6],
                "Fuel Type": dataset[7],
                "Body Type": dataset[8],
                "Price": dataset[9],
                "Link": dataset[10]
            })

    def startScraping(self):
        headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'
        }
        page_offset = 0
        page_counter = 1
        while True:
            print("Checking page {}".format(page_counter))
            page_counter += 1
            data = {
                "operationName": "getMarketplaceSearchChallenger",
                "variables": {
                    "filters": {
                        "condition": "USED",
                        "fallbackStrategy": "SIMPLE",
                        "excludeExpandedDelivery": False
                    },
                    "sort": "BEST_MATCH",
                    "first": 30,
                    "offset": page_offset,
                    "galleryImagesCount": 5,
                    "includeSeoInventorySummaryAndBodyStyles": False,
                    "includeSponsoredListings": False
                },
                "query": "query getMarketplaceSearchChallenger($filters: ListingSearchInput, $first: Int, $offset: Int, $sort: ListingsSort, $galleryImagesCount: Int, $includeSeoInventorySummaryAndBodyStyles: Boolean!, $includeSponsoredListings: Boolean!) {\n  listingSearch(filters: $filters, first: $first, offset: $offset, sort: $sort, createEvent: true) {\n    filters(includeZeros: true) {\n      truecarPlus {\n        options {\n          count\n          value\n          __typename\n        }\n        __typename\n      }\n      years {\n        min\n        max\n        __typename\n      }\n      price {\n        min\n        max\n        __typename\n      }\n      __typename\n    }\n    seoAggs {\n      price {\n        min\n        max\n        __typename\n      }\n      year {\n        min\n        max\n        __typename\n      }\n      bodyStyles {\n        label\n        value\n        count\n        __typename\n      }\n      fuelTypes {\n        label\n        value\n        count\n        __typename\n      }\n      cabTypes {\n        label\n        value\n        count\n        __typename\n      }\n      transmissions {\n        label\n        value\n        count\n        __typename\n      }\n      popularFeatures {\n        label\n        value\n        count\n        __typename\n      }\n      trims {\n        label\n        count\n        avgPrice\n        __typename\n      }\n      years {\n        edges {\n          cursor\n          node {\n            minPrice\n            year\n            excellentPrice\n            accidentFree\n            count\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      mileage @include(if: $includeSeoInventorySummaryAndBodyStyles) {\n        min\n        max\n        __typename\n      }\n      onlineOnlyDealers @include(if: $includeSeoInventorySummaryAndBodyStyles)\n      __typename\n    }\n    edges {\n      cursor\n      node {\n        vehicle {\n          vin\n          condition\n          make {\n            slug\n            name\n            id\n            __typename\n          }\n          model {\n            slug\n            name\n            id\n            __typename\n          }\n          style {\n            id\n            trim {\n              name\n              slug\n              id\n              __typename\n            }\n            name\n            driveType {\n              id\n              acronym\n              name\n              __typename\n            }\n            __typename\n          }\n          year\n          certifiedPreOwned\n          mileage\n          exteriorColorV2 {\n            __typename\n            ... on GenericColor {\n              genericName\n              name\n              __typename\n            }\n            ... on VehicleColor {\n              id\n              genericName\n              name\n              __typename\n            }\n          }\n          interiorColorV2 {\n            __typename\n            ... on GenericColor {\n              genericName\n              name\n              __typename\n            }\n            ... on VehicleColor {\n              id\n              genericName\n              name\n              __typename\n            }\n          }\n          conditionHistory {\n            ownerCount\n            accidentCount\n            isFleetCar\n            __typename\n          }\n          mpg {\n            city\n            highway\n            __typename\n          }\n          transmission\n          engine\n          fuelType\n          bodyStyle\n          __typename\n        }\n        id\n        dealership {\n          location {\n            id\n            geolocation {\n              postalCode\n              city\n              state\n              id\n              __typename\n            }\n            address1\n            address2\n            __typename\n          }\n          databaseId\n          id\n          parentDealershipName\n          __typename\n        }\n        isMultiLocation\n        distanceRetailing\n        tcplusEligible\n        galleryImages(first: $galleryImagesCount) {\n          nodes {\n            url\n            width\n            metadata\n            __typename\n          }\n          __typename\n        }\n        pricing {\n          exclusion\n          maapOverriddenAt\n          listPrice\n          priceBeforeDrop\n          discountLabel\n          deliveryFee\n          transferFee {\n            amount\n            fromCity\n            fromState\n            distance\n            __typename\n          }\n          totalMsrp\n          subTotal\n          __typename\n        }\n        consumerProspectedAt\n        marketAnalysis {\n          priceQuality\n          marketAverageAnalysis {\n            averageSaved\n            averagePricePercentage\n            averagePriceRange {\n              min\n              max\n              __typename\n            }\n            averagePrice\n            __typename\n          }\n          calloutDifferenceString\n          calloutPriceSavings\n          recentOfferAnalysis {\n            averageSaved\n            averagePricePercentage\n            averagePrice\n            transactionCount\n            averagePricePercentageRange {\n              min\n              max\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        precalculatedLease {\n          totalMonthlyPayment\n          disclaimer\n          dueAtSigning\n          mileage\n          term\n          __typename\n        }\n        precalculatedLoan {\n          totalMonthlyPayment\n          disclaimer\n          downPayment\n          term\n          __typename\n        }\n        highlightedOptionsOrKeyFeatures\n        __typename\n      }\n      hiddenListingsInfo {\n        hasHiddenListings\n        hiddenListingsKey\n        hiddenListingCount\n        __typename\n      }\n      distance {\n        miles\n        __typename\n      }\n      __typename\n    }\n    displayNames {\n      make {\n        name\n        __typename\n      }\n      model {\n        name\n        __typename\n      }\n      bodyStyle {\n        name\n        __typename\n      }\n      trim {\n        name\n        __typename\n      }\n      __typename\n    }\n    isFallback\n    totalCount\n    sponsoredListings @include(if: $includeSponsoredListings) {\n      cursor\n      node {\n        vehicle {\n          vin\n          condition\n          make {\n            id\n            slug\n            name\n            __typename\n          }\n          model {\n            id\n            slug\n            name\n            __typename\n          }\n          style {\n            id\n            trim {\n              id\n              name\n              __typename\n            }\n            name\n            driveType {\n              id\n              acronym\n              __typename\n            }\n            __typename\n          }\n          year\n          certifiedPreOwned\n          mileage\n          exteriorColorV2 {\n            __typename\n            ... on GenericColor {\n              genericName\n              name\n              __typename\n            }\n            ... on VehicleColor {\n              id\n              genericName\n              name\n              __typename\n            }\n          }\n          interiorColorV2 {\n            __typename\n            ... on GenericColor {\n              genericName\n              name\n              __typename\n            }\n            ... on VehicleColor {\n              id\n              genericName\n              name\n              __typename\n            }\n          }\n          conditionHistory {\n            ownerCount\n            accidentCount\n            isFleetCar\n            __typename\n          }\n          mpg {\n            city\n            highway\n            __typename\n          }\n          transmission\n          engine\n          __typename\n        }\n        id\n        isMultiLocation\n        distanceRetailing\n        dealership {\n          databaseId\n          location {\n            id\n            geolocation {\n              id\n              city\n              state\n              postalCode\n              __typename\n            }\n            address1\n            address2\n            __typename\n          }\n          id\n          parentDealershipName\n          __typename\n        }\n        tcplusEligible\n        galleryImages(first: $galleryImagesCount) {\n          nodes {\n            url\n            width\n            metadata\n            __typename\n          }\n          __typename\n        }\n        pricing {\n          exclusion\n          maapOverriddenAt\n          listPrice\n          priceBeforeDrop\n          discountLabel\n          deliveryFee\n          transferFee {\n            amount\n            fromCity\n            fromState\n            distance\n            __typename\n          }\n          totalMsrp\n          subTotal\n          __typename\n        }\n        consumerProspectedAt\n        marketAnalysis {\n          priceQuality\n          marketAverageAnalysis {\n            averageSaved\n            averagePricePercentage\n            averagePriceRange {\n              min\n              max\n              __typename\n            }\n            averagePrice\n            __typename\n          }\n          calloutDifferenceString\n          calloutPriceSavings\n          recentOfferAnalysis {\n            averageSaved\n            averagePricePercentage\n            averagePrice\n            transactionCount\n            averagePricePercentageRange {\n              min\n              max\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        precalculatedLease {\n          totalMonthlyPayment\n          disclaimer\n          dueAtSigning\n          mileage\n          term\n          __typename\n        }\n        precalculatedLoan {\n          totalMonthlyPayment\n          disclaimer\n          downPayment\n          term\n          __typename\n        }\n        highlightedOptionsOrKeyFeatures\n        __typename\n      }\n      hiddenListingsInfo {\n        hasHiddenListings\n        hiddenListingsKey\n        hiddenListingCount\n        __typename\n      }\n      distance {\n        miles\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
            }
            try:
                resp = requests.post(self.api_url, headers=headers,
                                     data=json.dumps(data)).json()
            except:
                print("Failed to open {}".format(self.api_url))
                return
            if len(resp.get('data').get('listingSearch').get('edges')) == 0:
                print("Reached last page! Stopping scraper ...")
                break
            self.processData(resp)
            page_offset += 30

    def processData(self, resp):
        all_cars = resp.get('data').get('listingSearch').get('edges')
        for car_data in all_cars:
            car = car_data.get('node')
            listing_id = car.get('id')
            decoded_listing_id = base64.b64decode(listing_id.encode('utf-8')).decode('utf-8')
            listing_link = "https://www.truecar.com/used-cars-for-sale/listing/{}"
            listing_id = "-".join(decoded_listing_id.split('-')[1::])
            listing_link = listing_link.format(listing_id)
            car_company = car.get('vehicle').get('make').get('name')
            car_model = car.get('vehicle').get('model').get('name')
            style_name = car.get('vehicle').get('style').get('name')
            year = car.get('vehicle').get('year')
            mileage = car.get('vehicle').get('mileage')
            transmission_type = car.get('vehicle').get('transmission')
            engine = car.get('vehicle').get('engine')
            fuel_type = car.get('vehicle').get('fuelType')
            body_type = car.get('vehicle').get('bodyStyle')
            price = car.get('pricing').get('listPrice')
            print("Listing URL: {}".format(listing_link))
            print("Car Company: {}".format(car_company))
            print("Car Model: {}".format(car_model))
            print("Style Name: {}".format(style_name))
            print("Year: {}".format(year))
            print("Mileage: {}".format(mileage))
            print("Transmission Type: {}".format(transmission_type))
            print("Engine: {}".format(engine))
            print("Fuel Type: {}".format(fuel_type))
            print("Body Type: {}".format(body_type))
            print("Price: {}".format(price))
            print("\n")
            dataset = [
                car_company,
                car_model,
                style_name,
                year,
                mileage,
                transmission_type,
                engine,
                fuel_type,
                body_type,
                price,
                listing_link
            ]
            self.saveData(dataset)


if __name__ == "__main__":
    scraper = TrueCar()
    scraper.startScraping()
