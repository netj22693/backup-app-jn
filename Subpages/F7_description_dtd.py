import streamlit as st



st.write("# Door-to-Door:")

''
st.write("This page provides a description about **delivery logic** in the Function 7.")

''
st.write("""
    - Principle:
         - You select delivery **From** city (A) **To** city (B)
         - The predefined cities can be seen like **hubs**
         - Based on the points **A** and **B**, the function will do **calculation of costs** based on **distance**
         """)

''
st.write("""
    - **But what about cases(!)**:
        1. When the real pick up/delivery point is **not** in the city?
        2. Or your transport type between the A and B is either **Train** or **Airplane** -> you also need to **get the shipment** from either **Station** or **Airport** to somewhere else?
    """)

''
with st.expander("Additional context", icon= ":material/info:"):
    st.write("""
        - Note to 1. point:
            - It is pretty common that industries, hubs, companies are around cities/close to cities
            - Or eventuelly your delivery point is some smaller city, place in the area close to the city          
    """)

    st.write("""
        - Note to 2. point:
            - Using a **Truck** as a transport you can **get almost everywhere** where road is      
            - But this is **not** the case for **Train** or **Airplane**
            - You need to have some way how to get a shipment on Train or on Airplane and how to get it off -> **You need to plan how to get the shipment to/from Station/Airport**. 
    """)


''
st.write("""
    - **Solution** - In the Function 7 you can select whether you need to **serve just the A to B distance** or you want the company to **do more** for you -> **Door-to-Door delivery**.
         """)

''
''
st.write("##### Area:")

st.write("""
    - **Truck**:
         - More flexible 
         - Includes City area for Free
         - Additional distance in area of 10 or 20 km is payed 
         """)

st.write("""
    - **Train** and **Airplane**:
         - Less flexible as you also need an extra Truck for the "first/last mile"
         - There is **a must to transfer the shipment**
         - Usually the Train hubs or Airports are not directly in the city -> the delivery area is 10 or 20 km (payed)
         """)

''
''
col1, col2 = st.columns(2)
col1.image("Pictures/Function_7/F7_dtd_area_truck.svg", width= 220)
col2.image("Pictures/Function_7/F7_dtd_area_train_air.svg", width= 250)

''
''
''
st.write("##### Examples:")
''
st.image("Pictures/Function_7/F7_dtd_legend.svg")
''

''
st.write("""
    **Example 1** - Only A to B delivery
    - **Selected transport**: Airplane (applicable also for Train)
    - **Case**: Customer wants just A to B delivery - Airplane
    - This means that the customer will ensure the delivery of the shipment to the Airport (A) and also ensure the pick up from the Airport (B)
    - **The payed service**: Airplane transfer from A to B
    """)

''
st.image("Pictures/Function_7/F7_dtd_ab_air.svg", width=400)


''
''
''
st.write("""
    **Example 2** - A to B delivery + B - 20 km
    - **Selected transport**: Airplane (applicable also for Train)
    - **Case**: Customer wants delivery to final destination in area of 20 km from airport
    - This means that the customer will ensure the delivery of the shipment to the Airport (A)
    - **The payed service**: Airplane transfer from A to B and transfer from Airplane to a Truck to deliver to the destination in area of 20 km from the Airport
    """)


st.image("Pictures/Function_7/F7_dtd_abb_air.svg", width=480)

''
''
''
st.write("""
    **Example 3** - A - 20 km + A to B delivery + B - 20 km
    - **Selected transport**: Train (applicable also for Airplane)
    - **Case**: Full road
    - **The payed service**: Pick up by Truck, delivery to Airport (A), transfer to Airport (B) by Airplane, transfer to Truck, delivery to final destination. **End-to-end payed**
    """)

''
st.image("Pictures/Function_7/F7_dtd_aabb_train.svg", width=480)


''
''
''
st.write("""
    **Example 4 (Different view)** - A to B delivery + B - 20 km
    - **Selected transport**: Train (applicable also for Airplane)
    - **Case**: Customer will ensure delivery to the Train Station/hub
    - **The payed service**: Delivery from Train Station (A) to Train Station (B), transfer to Truck, delivery to final destination
    """)

st.image("Pictures/Function_7/F7_dtd_cargo_transfer.svg", width=450)

''
''
''
st.write("""
    **Example 5 (Different view)** - A - 10 km + A to B delivery
    - **Selected transport**: Airplane (applicable also for Train)
    - **Case**: Customer will ensure pick up from to the Train Station/hub
    - **The payed service**: Pick up by Truck, delivery to Airport (A), delivery to Airport (B) by Airplane
    """)

''
st.image("Pictures/Function_7/F7_dtd_cargo_air.svg", width=600)

''
''
''
st.write("""
    **Example 6** - A - 20 km + A to B delivery
    - **Selected transport**: Truck
    - **Case**: End-to-end delivery - B point in the city area
    - **The payed service**: End-to-end covered by Truck
    """)

''
st.image("Pictures/Function_7/F7_dtd_aab_truck.svg", width=400)


''
''
''
''
st.write("""
    **Conclusion**:
    - All the three transport types (Truck, Train, Airplane) allows the same type of pick up/delivery:
         - A to B only 
         - A -> A to B
         - A to B -> B
         - A -> A to B -> B
    """)

st.write("""
    - **Truck** is more flexible thus has circles of delivery
         - Within city - everywhere in the city for free
         - 10 km area of the city edge 
         - 20 km area of the city edge
    """)

''
st.write("""
    - **Train** and **Airplane**, due to Stations/Hubs/Airports are commonly not in the cities (so for "first/last mile" Truck needed), the offer is:
         - No - just Train/Airplane transfare A to B
         - 10 km area of pick up/delivery
         - 20 km area of pick up/delivery
    """)


# ===== Page navigation at the bottom ======
''
''
''
''
st.write("-------")

st.page_link(
	label = "Function 7",
	page="Subpages/F7_FUNCTION_transport.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
	icon=":material/play_circle:"
	) 

st.page_link(
    label = "Previous page",
	page="Subpages/F7_description.py",
	help="The button will redirect to the relevant page within this app.",
	use_container_width=True,
    icon=":material/west:",
	) 
