import json
import csv

files=[open("maojson_1.json"),open("maojson_2.json"),open('maojson_5.json'), open("auth_mismatch_with_tax.json")]
for single_file in files:
    data = json.load(single_file)
    if data["IsConfirmed"]==True:
        OrderStatus='Placed Successfully'
    else:
        OrderStatus="IsOnHold"
    Price_Without_Taxs=0
    for Price_Without_Tax in data["OrderLine"]:
        Price_Without_Taxs = round(Price_Without_Taxs + Price_Without_Tax["UnitPrice"], 2)
    shippingcharge=0
    for shipping in data["OrderChargeDetail"]:
        shippingcharge=shippingcharge+shipping["ChargeTotal"]
        # print("ships",shippingcharge)

    taxes = 0
    for tax in data["OrderTaxDetail"]:
        # print(tax)
        taxes = taxes + tax["TaxAmount"]
        # print("taxes", taxes)
    # shipstaxs = data["OrderLine"]
    shipstax=0
    for ships1 in data["OrderLine"]:
        for ship in ships1["OrderLineTaxDetail"]:
            shipstax = shipstax +ship["TaxAmount"]
            # print("ship", shipstax)

    totaltax=round((Price_Without_Taxs+shippingcharge+shipstax+taxes),2)

    # print(total)
    total_amount = data["Payment"][0]["PaymentMethod"][0]["Amount"]
    difference=int(total_amount-totaltax)
    payment=data["Extended"]["PrimaryPaymentMethod"]
    pay = data["Payment"]
    payment_count = 0
    credit_card = 0
    paypal = 0
    for way_pay in pay:
        for pay_type in way_pay["PaymentMethod"]:
            if "Credit Card" in pay_type["PaymentType"].values():
                payment_count += 1
                credit_card += 1
            elif "PayPal" in pay_type["PaymentType"].values():
                payment_count += 1
                paypal += 1
            elif "Gift Card" in pay_type["PaymentType"].values():
                payment_count += 1
            elif "Loyalty Certificate" in pay_type["PaymentType"].values():
                payment_count += 1
    name = (data["CapturedDate"], data["OrderId"],OrderStatus,Price_Without_Taxs,totaltax,total_amount,difference,payment,payment_count)
    for names in name:
        print(names)
    data_file = open('auth_0208.csv', 'a', newline='')
    csv_writer = csv.writer(data_file)
    csv_writer.writerow(name)
    data_file.close()