import json
import random

class FastFoodProductGenerator:
    def __init__(self):
        self.products = []
        
        # Categories to generate (10 each = 100 total)
        self.categories = [
            "Burgers", "Pizza", "Fried Chicken", "Tacos & Wraps", "Sides & Appetizers",
            "Beverages", "Desserts", "Salads & Healthy Options", "Breakfast Items", "Limited Time Specials"
        ]
        
        self.product_templates = {
            "Burgers": [
                {"name": "Spicy Dragon Fusion Burger", "desc": "Korean gochujang meets American beef with kimchi slaw", "ingredients": ["beef patty", "gochujang sauce", "kimchi", "brioche bun"], "price": 12.99, "spice": 7},
                {"name": "BBQ Bacon Smash Burger", "desc": "Double smashed patties with crispy bacon and BBQ sauce", "ingredients": ["double beef patty", "bacon", "BBQ sauce", "cheddar", "onion"], "price": 11.49, "spice": 3},
                {"name": "Mediterranean Lamb Burger", "desc": "Seasoned lamb with feta, cucumber, and tzatziki", "ingredients": ["lamb patty", "feta cheese", "cucumber", "tzatziki", "pita bun"], "price": 13.99, "spice": 2},
                {"name": "Nashville Hot Chicken Burger", "desc": "Fried chicken with Nashville hot sauce and pickles", "ingredients": ["fried chicken breast", "hot sauce", "pickles", "mayo", "brioche"], "price": 10.99, "spice": 8},
                {"name": "Truffle Mushroom Swiss Burger", "desc": "Beef patty with sautéed mushrooms and truffle aioli", "ingredients": ["beef patty", "swiss cheese", "mushrooms", "truffle aioli", "arugula"], "price": 14.49, "spice": 1},
                {"name": "Jalapeño Popper Burger", "desc": "Beef burger with jalapeño cream cheese and bacon", "ingredients": ["beef patty", "jalapeños", "cream cheese", "bacon", "sesame bun"], "price": 11.99, "spice": 6},
                {"name": "Veggie Black Bean Burger", "desc": "House-made black bean patty with avocado", "ingredients": ["black bean patty", "avocado", "sprouts", "chipotle mayo", "whole grain bun"], "price": 9.99, "spice": 4},
                {"name": "Buffalo Chicken Ranch Burger", "desc": "Grilled chicken with buffalo sauce and ranch", "ingredients": ["chicken breast", "buffalo sauce", "ranch", "lettuce", "tomato"], "price": 10.49, "spice": 5},
                {"name": "Breakfast Burger Deluxe", "desc": "Beef patty topped with fried egg and hash browns", "ingredients": ["beef patty", "fried egg", "hash browns", "bacon", "hollandaise"], "price": 12.49, "spice": 2},
                {"name": "Asian Fusion Teriyaki Burger", "desc": "Beef with teriyaki glaze, pineapple, and wasabi mayo", "ingredients": ["beef patty", "teriyaki sauce", "pineapple", "wasabi mayo", "sesame seeds"], "price": 11.99, "spice": 3}
            ],
            "Pizza": [
                {"name": "Detroit Style Pepperoni Square", "desc": "Thick crust pizza with crispy pepperoni cups", "ingredients": ["thick dough", "pepperoni", "mozzarella", "tomato sauce"], "price": 15.99, "spice": 2},
                {"name": "Thai Chicken Curry Pizza", "desc": "Curry sauce base with chicken and Thai basil", "ingredients": ["curry sauce", "chicken", "thai basil", "red peppers", "coconut"], "price": 17.49, "spice": 6},
                {"name": "Truffle Mac & Cheese Pizza", "desc": "White sauce with mac and cheese and truffle oil", "ingredients": ["white sauce", "macaroni", "cheese blend", "truffle oil", "breadcrumbs"], "price": 18.99, "spice": 1},
                {"name": "Mexican Street Corn Pizza", "desc": "Charred corn with lime crema and cotija cheese", "ingredients": ["corn", "lime crema", "cotija cheese", "cilantro", "chili powder"], "price": 16.49, "spice": 4},
                {"name": "Korean BBQ Bulgogi Pizza", "desc": "Marinated beef with kimchi and scallions", "ingredients": ["bulgogi beef", "kimchi", "scallions", "sesame oil", "gochujang drizzle"], "price": 19.99, "spice": 7},
                {"name": "Buffalo Chicken Ranch Pizza", "desc": "Buffalo chicken with ranch and celery", "ingredients": ["buffalo chicken", "ranch", "celery", "blue cheese", "hot sauce"], "price": 16.99, "spice": 5},
                {"name": "Mediterranean Veggie Delight", "desc": "Olives, sun-dried tomatoes, and goat cheese", "ingredients": ["olives", "sun-dried tomatoes", "goat cheese", "spinach", "balsamic"], "price": 15.49, "spice": 1},
                {"name": "Smoky BBQ Brisket Pizza", "desc": "Slow-cooked brisket with BBQ sauce and onions", "ingredients": ["brisket", "BBQ sauce", "red onions", "smoked gouda", "cilantro"], "price": 18.49, "spice": 3},
                {"name": "Breakfast Pizza Supreme", "desc": "Scrambled eggs, bacon, sausage, and hash browns", "ingredients": ["scrambled eggs", "bacon", "sausage", "hash browns", "hollandaise"], "price": 17.99, "spice": 2},
                {"name": "Pesto Chicken Arugula Pizza", "desc": "Basil pesto with grilled chicken and fresh arugula", "ingredients": ["basil pesto", "grilled chicken", "arugula", "pine nuts", "parmesan"], "price": 16.99, "spice": 1}
            ],
            "Fried Chicken": [
                {"name": "Korean Fried Chicken Wings", "desc": "Double-fried wings with gochujang glaze", "ingredients": ["chicken wings", "gochujang", "sesame seeds", "scallions"], "price": 13.99, "spice": 8},
                {"name": "Nashville Hot Tenders", "desc": "Hand-breaded tenders with fiery Nashville seasoning", "ingredients": ["chicken tenders", "nashville seasoning", "pickles", "ranch"], "price": 11.49, "spice": 9},
                {"name": "Honey Sriracha Glazed Wings", "desc": "Crispy wings with sweet and spicy honey sriracha", "ingredients": ["chicken wings", "honey", "sriracha", "butter", "cilantro"], "price": 12.99, "spice": 6},
                {"name": "Buffalo Cauliflower Bites", "desc": "Crispy cauliflower tossed in buffalo sauce", "ingredients": ["cauliflower", "buffalo sauce", "ranch", "celery salt"], "price": 9.99, "spice": 5},
                {"name": "Japanese Karaage Chicken", "desc": "Light and crispy Japanese-style fried chicken", "ingredients": ["chicken thighs", "potato starch", "soy sauce", "ginger", "garlic"], "price": 10.99, "spice": 2},
                {"name": "Cajun Spiced Chicken Sandwich", "desc": "Blackened chicken breast with remoulade sauce", "ingredients": ["chicken breast", "cajun spices", "remoulade", "lettuce", "tomato"], "price": 11.99, "spice": 7},
                {"name": "Buttermilk Fried Chicken Bucket", "desc": "Classic buttermilk fried chicken pieces", "ingredients": ["chicken pieces", "buttermilk", "flour", "herbs", "spices"], "price": 18.99, "spice": 3},
                {"name": "Thai Basil Chicken Wings", "desc": "Wings with Thai basil, chili, and fish sauce", "ingredients": ["chicken wings", "thai basil", "chilies", "fish sauce", "lime"], "price": 13.49, "spice": 8},
                {"name": "Lemon Pepper Wings", "desc": "Crispy wings with zesty lemon pepper seasoning", "ingredients": ["chicken wings", "lemon pepper", "butter", "parsley"], "price": 11.99, "spice": 2},
                {"name": "Chicken & Waffles Deluxe", "desc": "Fried chicken served with Belgian waffles", "ingredients": ["fried chicken", "belgian waffles", "maple syrup", "butter"], "price": 14.99, "spice": 1}
            ],
            "Tacos & Wraps": [
                {"name": "Korean BBQ Bulgogi Tacos", "desc": "Marinated beef with kimchi and gochujang crema", "ingredients": ["bulgogi beef", "kimchi", "gochujang crema", "corn tortillas"], "price": 9.99, "spice": 6},
                {"name": "Fish Tacos Baja Style", "desc": "Beer-battered fish with cabbage slaw and lime", "ingredients": ["beer-battered fish", "cabbage slaw", "lime crema", "pico de gallo"], "price": 11.49, "spice": 3},
                {"name": "Nashville Hot Chicken Wrap", "desc": "Spicy fried chicken in flour tortilla with ranch", "ingredients": ["fried chicken", "nashville sauce", "lettuce", "ranch", "flour tortilla"], "price": 10.99, "spice": 8},
                {"name": "Mediterranean Lamb Gyro", "desc": "Seasoned lamb with tzatziki and fresh vegetables", "ingredients": ["lamb", "tzatziki", "tomatoes", "onions", "pita bread"], "price": 12.99, "spice": 2},
                {"name": "Buffalo Chicken Caesar Wrap", "desc": "Buffalo chicken with caesar dressing and parmesan", "ingredients": ["buffalo chicken", "caesar dressing", "parmesan", "romaine", "tortilla"], "price": 9.49, "spice": 5},
                {"name": "Carnitas Street Tacos", "desc": "Slow-cooked pork with onions and cilantro", "ingredients": ["carnitas", "onions", "cilantro", "lime", "corn tortillas"], "price": 8.99, "spice": 4},
                {"name": "Thai Chicken Lettuce Wraps", "desc": "Ground chicken with Thai herbs in lettuce cups", "ingredients": ["ground chicken", "thai herbs", "peanuts", "lime", "lettuce cups"], "price": 10.49, "spice": 6},
                {"name": "Breakfast Burrito Supreme", "desc": "Scrambled eggs, bacon, potatoes, and cheese", "ingredients": ["scrambled eggs", "bacon", "potatoes", "cheese", "salsa"], "price": 8.49, "spice": 3},
                {"name": "Veggie Buddha Bowl Wrap", "desc": "Quinoa, roasted vegetables, and tahini dressing", "ingredients": ["quinoa", "roasted vegetables", "tahini", "spinach", "whole wheat tortilla"], "price": 9.99, "spice": 1},
                {"name": "Cuban Mojo Pork Wrap", "desc": "Citrus-marinated pork with pickles and mustard", "ingredients": ["mojo pork", "pickles", "mustard", "swiss cheese", "pressed tortilla"], "price": 11.99, "spice": 2}
            ],
            "Sides & Appetizers": [
                {"name": "Loaded Kimchi Fries", "desc": "Crispy fries topped with kimchi and gochujang aioli", "ingredients": ["fries", "kimchi", "gochujang aioli", "sesame seeds", "scallions"], "price": 7.99, "spice": 7},
                {"name": "Truffle Parmesan Fries", "desc": "Hand-cut fries with truffle oil and parmesan", "ingredients": ["hand-cut fries", "truffle oil", "parmesan", "herbs"], "price": 8.99, "spice": 1},
                {"name": "Buffalo Chicken Dip", "desc": "Creamy buffalo chicken dip with tortilla chips", "ingredients": ["chicken", "cream cheese", "buffalo sauce", "cheese", "tortilla chips"], "price": 9.49, "spice": 5},
                {"name": "Japanese Gyoza Dumplings", "desc": "Pan-fried pork dumplings with ponzu dipping sauce", "ingredients": ["pork", "dumpling wrappers", "ponzu sauce", "ginger", "scallions"], "price": 8.49, "spice": 2},
                {"name": "Jalapeño Poppers Deluxe", "desc": "Bacon-wrapped jalapeños stuffed with cream cheese", "ingredients": ["jalapeños", "cream cheese", "bacon", "ranch dipping sauce"], "price": 7.49, "spice": 6},
                {"name": "Sweet Potato Fries", "desc": "Crispy sweet potato fries with chipotle mayo", "ingredients": ["sweet potatoes", "chipotle mayo", "sea salt"], "price": 6.99, "spice": 3},
                {"name": "Mozzarella Sticks Gourmet", "desc": "Hand-breaded mozzarella with marinara sauce", "ingredients": ["mozzarella", "breadcrumbs", "marinara sauce", "italian herbs"], "price": 7.99, "spice": 1},
                {"name": "Korean Corn Dogs", "desc": "Hot dogs coated in potato cubes and fried", "ingredients": ["hot dogs", "potato cubes", "corn batter", "mustard"], "price": 6.49, "spice": 2},
                {"name": "Loaded Nachos Supreme", "desc": "Tortilla chips with cheese, jalapeños, and toppings", "ingredients": ["tortilla chips", "cheese sauce", "jalapeños", "sour cream", "guacamole"], "price": 11.99, "spice": 4},
                {"name": "Coconut Shrimp Bites", "desc": "Crispy coconut-crusted shrimp with mango salsa", "ingredients": ["shrimp", "coconut", "mango salsa", "sweet chili sauce"], "price": 10.99, "spice": 2}
            ],
            "Beverages": [
                {"name": "Korean Strawberry Milk", "desc": "Sweet strawberry milk with real fruit pieces", "ingredients": ["milk", "strawberries", "sugar", "ice"], "price": 4.99, "spice": 0},
                {"name": "Thai Iced Tea", "desc": "Traditional Thai tea with condensed milk", "ingredients": ["thai tea", "condensed milk", "ice", "sugar"], "price": 3.99, "spice": 0},
                {"name": "Mango Lassi Smoothie", "desc": "Creamy mango yogurt drink with cardamom", "ingredients": ["mango", "yogurt", "cardamom", "honey"], "price": 5.49, "spice": 0},
                {"name": "Horchata Milkshake", "desc": "Cinnamon rice drink blended with vanilla ice cream", "ingredients": ["rice milk", "cinnamon", "vanilla ice cream", "sugar"], "price": 5.99, "spice": 0},
                {"name": "Green Tea Matcha Latte", "desc": "Ceremonial grade matcha with steamed milk", "ingredients": ["matcha powder", "steamed milk", "honey"], "price": 4.49, "spice": 0},
                {"name": "Craft Root Beer Float", "desc": "House-made root beer with vanilla ice cream", "ingredients": ["craft root beer", "vanilla ice cream"], "price": 4.99, "spice": 0},
                {"name": "Fresh Lemonade Fusion", "desc": "House-made lemonade with mint and berries", "ingredients": ["fresh lemons", "mint", "mixed berries", "sparkling water"], "price": 3.99, "spice": 0},
                {"name": "Vietnamese Iced Coffee", "desc": "Strong coffee with sweetened condensed milk", "ingredients": ["vietnamese coffee", "condensed milk", "ice"], "price": 4.49, "spice": 0},
                {"name": "Hibiscus Berry Refresher", "desc": "Tart hibiscus tea with mixed berry flavors", "ingredients": ["hibiscus tea", "mixed berries", "agave", "sparkling water"], "price": 4.29, "spice": 0},
                {"name": "Chocolate Peanut Butter Shake", "desc": "Rich chocolate shake with peanut butter swirl", "ingredients": ["chocolate ice cream", "peanut butter", "milk", "whipped cream"], "price": 6.49, "spice": 0}
            ],
            "Desserts": [
                {"name": "Korean Bingsu Ice Cream", "desc": "Shaved ice with red bean and condensed milk", "ingredients": ["shaved ice", "red bean", "condensed milk", "mochi"], "price": 7.99, "spice": 0},
                {"name": "Churros with Dulce de Leche", "desc": "Cinnamon sugar churros with caramel dipping sauce", "ingredients": ["churros", "cinnamon sugar", "dulce de leche"], "price": 6.99, "spice": 0},
                {"name": "Thai Mango Sticky Rice", "desc": "Sweet sticky rice with fresh mango slices", "ingredients": ["sticky rice", "mango", "coconut milk", "sesame seeds"], "price": 6.49, "spice": 0},
                {"name": "Japanese Mochi Ice Cream", "desc": "Traditional mochi filled with premium ice cream", "ingredients": ["mochi", "ice cream", "rice flour"], "price": 5.99, "spice": 0},
                {"name": "New York Cheesecake Bites", "desc": "Mini cheesecake bites with berry compote", "ingredients": ["cream cheese", "graham crackers", "berry compote"], "price": 7.49, "spice": 0},
                {"name": "Fried Ice Cream Sundae", "desc": "Tempura-fried ice cream with honey drizzle", "ingredients": ["vanilla ice cream", "tempura batter", "honey", "cinnamon"], "price": 8.99, "spice": 0},
                {"name": "Tres Leches Cake Slice", "desc": "Sponge cake soaked in three types of milk", "ingredients": ["sponge cake", "evaporated milk", "condensed milk", "heavy cream"], "price": 6.99, "spice": 0},
                {"name": "Chocolate Lava Cake", "desc": "Warm chocolate cake with molten center", "ingredients": ["chocolate", "butter", "eggs", "flour", "vanilla ice cream"], "price": 8.49, "spice": 0},
                {"name": "Baklava Cheesecake Fusion", "desc": "Greek baklava meets New York cheesecake", "ingredients": ["phyllo dough", "cream cheese", "honey", "pistachios"], "price": 7.99, "spice": 0},
                {"name": "Banana Foster Bread Pudding", "desc": "Warm bread pudding with banana foster sauce", "ingredients": ["bread pudding", "bananas", "rum sauce", "vanilla ice cream"], "price": 7.49, "spice": 0}
            ],
            "Salads & Healthy Options": [
                {"name": "Korean BBQ Beef Salad Bowl", "desc": "Mixed greens with bulgogi beef and gochujang dressing", "ingredients": ["mixed greens", "bulgogi beef", "gochujang dressing", "sesame seeds"], "price": 12.99, "spice": 5},
                {"name": "Mediterranean Quinoa Power Bowl", "desc": "Quinoa with chickpeas, olives, and tahini dressing", "ingredients": ["quinoa", "chickpeas", "olives", "tahini dressing", "cucumber"], "price": 11.49, "spice": 1},
                {"name": "Thai Beef Larb Salad", "desc": "Spicy ground beef with herbs and lime dressing", "ingredients": ["ground beef", "thai herbs", "lime dressing", "lettuce cups"], "price": 10.99, "spice": 8},
                {"name": "Poke Bowl Ahi Tuna", "desc": "Fresh ahi tuna with rice and Asian vegetables", "ingredients": ["ahi tuna", "sushi rice", "avocado", "seaweed", "ponzu"], "price": 14.99, "spice": 2},
                {"name": "Mexican Street Corn Salad", "desc": "Charred corn with cotija cheese and lime", "ingredients": ["corn", "cotija cheese", "lime", "chili powder", "cilantro"], "price": 8.99, "spice": 4},
                {"name": "Buffalo Chicken Cobb Salad", "desc": "Mixed greens with buffalo chicken and blue cheese", "ingredients": ["mixed greens", "buffalo chicken", "blue cheese", "tomatoes", "bacon"], "price": 11.99, "spice": 5},
                {"name": "Superfood Acai Bowl", "desc": "Acai base with granola, berries, and coconut", "ingredients": ["acai puree", "granola", "mixed berries", "coconut flakes"], "price": 9.99, "spice": 0},
                {"name": "Asian Fusion Chicken Salad", "desc": "Grilled chicken with Asian slaw and peanut dressing", "ingredients": ["grilled chicken", "asian slaw", "peanut dressing", "mint"], "price": 10.49, "spice": 3},
                {"name": "Greek Village Salad", "desc": "Traditional Greek salad with feta and olives", "ingredients": ["tomatoes", "cucumbers", "feta cheese", "olives", "olive oil"], "price": 9.49, "spice": 1},
                {"name": "Cauliflower Rice Buddha Bowl", "desc": "Cauliflower rice with roasted vegetables and tahini", "ingredients": ["cauliflower rice", "roasted vegetables", "tahini", "hemp seeds"], "price": 10.99, "spice": 1}
            ],
            "Breakfast Items": [
                {"name": "Korean Breakfast Sandwich", "desc": "Bulgogi beef with fried egg on brioche", "ingredients": ["bulgogi beef", "fried egg", "brioche bun", "kimchi"], "price": 9.99, "spice": 4},
                {"name": "Chilaquiles Benedict", "desc": "Poached eggs over tortilla chips with hollandaise", "ingredients": ["poached eggs", "tortilla chips", "hollandaise", "salsa verde"], "price": 11.49, "spice": 5},
                {"name": "Thai Basil Fried Rice", "desc": "Breakfast fried rice with thai basil and fried egg", "ingredients": ["jasmine rice", "thai basil", "fried egg", "fish sauce"], "price": 8.99, "spice": 6},
                {"name": "Breakfast Poutine Deluxe", "desc": "Hash browns with gravy, cheese curds, and bacon", "ingredients": ["hash browns", "gravy", "cheese curds", "bacon", "scallions"], "price": 10.99, "spice": 1},
                {"name": "Japanese Pancake Stack", "desc": "Fluffy Japanese pancakes with matcha butter", "ingredients": ["japanese pancakes", "matcha butter", "maple syrup", "berries"], "price": 12.99, "spice": 0},
                {"name": "Mexican Breakfast Bowl", "desc": "Rice and beans with chorizo and fried egg", "ingredients": ["rice", "black beans", "chorizo", "fried egg", "avocado"], "price": 9.49, "spice": 6},
                {"name": "French Toast Bread Pudding", "desc": "Brioche bread pudding with cinnamon and berries", "ingredients": ["brioche", "custard", "cinnamon", "mixed berries", "syrup"], "price": 8.99, "spice": 0},
                {"name": "Breakfast Ramen Bowl", "desc": "Ramen with soft egg, bacon, and scallions", "ingredients": ["ramen noodles", "soft egg", "bacon", "scallions", "miso broth"], "price": 11.99, "spice": 2},
                {"name": "Avocado Toast Deluxe", "desc": "Multigrain toast with avocado, egg, and everything seasoning", "ingredients": ["multigrain bread", "avocado", "fried egg", "everything seasoning"], "price": 8.49, "spice": 1},
                {"name": "Breakfast Quesadilla", "desc": "Flour tortilla with eggs, cheese, and breakfast meats", "ingredients": ["flour tortilla", "scrambled eggs", "cheese", "bacon", "sausage"], "price": 8.99, "spice": 3}
            ],
            "Limited Time Specials": [
                {"name": "Pumpkin Spice Burger", "desc": "Seasonal burger with pumpkin spice aioli and roasted squash", "ingredients": ["beef patty", "pumpkin spice aioli", "roasted squash", "arugula"], "price": 13.99, "spice": 2},
                {"name": "Holiday Cranberry Turkey Wrap", "desc": "Roasted turkey with cranberry sauce and stuffing", "ingredients": ["roasted turkey", "cranberry sauce", "stuffing", "spinach", "tortilla"], "price": 11.99, "spice": 1},
                {"name": "Summer Watermelon Feta Salad", "desc": "Fresh watermelon with feta cheese and mint", "ingredients": ["watermelon", "feta cheese", "mint", "balsamic glaze", "mixed greens"], "price": 9.99, "spice": 0},
                {"name": "Valentine's Day Red Velvet Shake", "desc": "Red velvet cake blended with vanilla ice cream", "ingredients": ["red velvet cake", "vanilla ice cream", "cream cheese", "milk"], "price": 6.99, "spice": 0},
                {"name": "St. Patrick's Day Irish Coffee", "desc": "Coffee with Irish whiskey flavor and whipped cream", "ingredients": ["coffee", "irish whiskey flavor", "whipped cream", "sugar"], "price": 5.49, "spice": 0},
                {"name": "Summer Mango Habanero Wings", "desc": "Wings with sweet mango and spicy habanero glaze", "ingredients": ["chicken wings", "mango", "habanero", "cilantro"], "price": 13.99, "spice": 9},
                {"name": "Fall Apple Cider Donuts", "desc": "Warm cider donuts with cinnamon sugar coating", "ingredients": ["apple cider", "donuts", "cinnamon sugar", "caramel drizzle"], "price": 5.99, "spice": 0},
                {"name": "Winter Peppermint Hot Chocolate", "desc": "Rich hot chocolate with peppermint and marshmallows", "ingredients": ["hot chocolate", "peppermint", "marshmallows", "whipped cream"], "price": 4.99, "spice": 0},
                {"name": "Spring Asparagus Risotto", "desc": "Creamy risotto with fresh asparagus and parmesan", "ingredients": ["arborio rice", "asparagus", "parmesan", "white wine"], "price": 14.99, "spice": 1},
                {"name": "Summer BBQ Pulled Pork Nachos", "desc": "Tortilla chips with pulled pork and BBQ sauce", "ingredients": ["tortilla chips", "pulled pork", "BBQ sauce", "cheese", "jalapeños"], "price": 12.99, "spice": 4}
            ]
        }

    def generate_product(self, category, product_data, product_id):
        """Generate a single product with proper formatting"""
        
        # Calculate calories based on ingredients and category
        base_calories = {
            "Burgers": 550, "Pizza": 650, "Fried Chicken": 420, "Tacos & Wraps": 380,
            "Sides & Appetizers": 320, "Beverages": 150, "Desserts": 380,
            "Salads & Healthy Options": 280, "Breakfast Items": 450, "Limited Time Specials": 480
        }
        
        calories = base_calories.get(category, 400) + random.randint(-100, 200)
        
        # Generate dietary tags based on ingredients
        dietary_tags = []
        ingredients_str = " ".join(product_data["ingredients"]).lower()
        
        if any(meat in ingredients_str for meat in ["beef", "chicken", "pork", "lamb", "turkey"]):
            if "chicken" in ingredients_str or "turkey" in ingredients_str:
                dietary_tags.append("lean_protein")
        else:
            dietary_tags.append("vegetarian")
            
        if product_data["spice"] >= 6:
            dietary_tags.append("spicy")
        elif product_data["spice"] >= 3:
            dietary_tags.append("mildly_spicy")
            
        if any(healthy in ingredients_str for healthy in ["quinoa", "salad", "vegetables", "avocado"]):
            dietary_tags.append("healthy")
            
        if product_data["price"] >= 12:
            dietary_tags.append("premium")
        elif product_data["price"] <= 7:
            dietary_tags.append("value")
            
        # Generate mood tags
        mood_tags = ["satisfying"]
        if product_data["spice"] >= 6:
            mood_tags.extend(["adventurous", "bold"])
        else:
            mood_tags.extend(["comfort", "familiar"])
            
        if category in ["Desserts", "Beverages"]:
            mood_tags.append("indulgent")
        elif category == "Salads & Healthy Options":
            mood_tags.extend(["refreshing", "energizing"])
            
        # Generate allergens
        allergens = []
        if any(gluten in ingredients_str for gluten in ["bun", "bread", "flour", "noodles"]):
            allergens.append("gluten")
        if any(dairy in ingredients_str for dairy in ["cheese", "milk", "cream", "butter"]):
            allergens.append("dairy")
        if "egg" in ingredients_str:
            allergens.append("eggs")
        if any(nut in ingredients_str for nut in ["peanut", "almond", "walnut"]):
            allergens.append("nuts")
            
        return {
            "product_id": f"FF{str(product_id).zfill(3)}",
            "name": product_data["name"],
            "category": category,
            "description": product_data["desc"],
            "ingredients": product_data["ingredients"],
            "price": product_data["price"],
            "calories": calories,
            "prep_time": f"{random.randint(3, 12)}-{random.randint(13, 20)} mins",
            "dietary_tags": dietary_tags,
            "mood_tags": mood_tags,
            "allergens": allergens,
            "popularity_score": random.randint(60, 95),
            "chef_special": random.choice([True, False]) if product_data["price"] >= 12 else False,
            "limited_time": category == "Limited Time Specials",
            "spice_level": product_data["spice"],
            "image_prompt": f"{category.lower()} {product_data['name'].lower()} food photography"
        }

    def generate_all_products(self):
        """Generate all 100 products"""
        print("🚀 Starting product generation...")
        print("📊 Generating 10 products each for 10 categories = 100 total")
        
        product_id = 1
        
        for category in self.categories:
            print(f"\n🍽️  Generating {category} products...")
            
            templates = self.product_templates[category]
            for i, template in enumerate(templates):
                product = self.generate_product(category, template, product_id)
                self.products.append(product)
                print(f"✅ Generated: {product['name']}")
                product_id += 1
        
        print(f"\n🎉 Successfully generated {len(self.products)} products!")
        return self.products

    def save_to_json(self, filename="fast_food_products.json"):
        """Save products to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, indent=2, ensure_ascii=False)
        print(f"💾 Products saved to {filename}")

    def display_sample_products(self, count=5):
        """Display sample products for verification"""
        print(f"\n📋 Sample Products (showing {count}):")
        for i, product in enumerate(self.products[:count]):
            print(f"\n--- Product {i+1} ---")
            print(f"ID: {product['product_id']}")
            print(f"Name: {product['name']}")
            print(f"Category: {product['category']}")
            print(f"Price: ${product['price']}")
            print(f"Spice Level: {product['spice_level']}/10")
            print(f"Description: {product['description'][:80]}...")

def main():
    print("🍔 FoodieBot Product Generator")
    print("===============================")
    print("Using creative product templates")
    print("(Compliant with assignment requirements)")
    
    # Initialize generator
    generator = FastFoodProductGenerator()
    
    # Generate all products
    products = generator.generate_all_products()
    
    # Save to file
    generator.save_to_json("fast_food_products.json")
    
    # Show samples
    generator.display_sample_products(5)
    
    # Show category breakdown
    print(f"\n📊 Category Breakdown:")
    for category in generator.categories:
        category_products = [p for p in products if p['category'] == category]
        print(f"   {category}: {len(category_products)} products")
    
    print(f"\n✅ COMPLETE! Your 100 fast food products are ready!")
    print(f"📁 File saved: fast_food_products.json")
    print(f"🎯 Ready for Phase 2: Database Setup!")

if __name__ == "__main__":
    main()