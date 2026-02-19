# Schema.org Recipe format

Reference for [Schema.org Recipe](https://schema.org/Recipe) JSON-LD format, used for web publishing and SEO.

## Basic structure

```json
{
  "@context": "https://schema.org",
  "@type": "Recipe",
  "name": "Recipe Title",
  "description": "Short description",
  "recipeIngredient": [...],
  "recipeInstructions": [...]
}
```

## Core fields

| Field | Type | Notes |
|-------|------|-------|
| `name` | String | Recipe title |
| `description` | String | Short description |
| `author` | String or Person | Recipe creator |
| `datePublished` | Date | ISO 8601 date (e.g., `2024-01-15`) |
| `image` | URL or ImageObject | Recipe photo |
| `recipeYield` | String | Servings (e.g., "4 servings", "1 loaf") |
| `recipeCategory` | String | Category (e.g., "appetizer", "dessert") |
| `recipeCuisine` | String | Cuisine type (e.g., "Italian", "Thai") |
| `keywords` | String | Comma-separated tags |

## Time fields

Use [ISO 8601 duration format](https://en.wikipedia.org/wiki/ISO_8601#Durations):

| Field | Example |
|-------|---------|
| `prepTime` | `PT15M` (15 minutes) |
| `cookTime` | `PT1H` (1 hour) |
| `totalTime` | `PT1H30M` (1 hour 30 minutes) |

Duration format: `PT[hours]H[minutes]M[seconds]S`
- `PT30M` = 30 minutes
- `PT2H` = 2 hours
- `PT1H45M` = 1 hour 45 minutes

## Ingredients

`recipeIngredient` is an array. Can be strings or PropertyValue objects:

```json
"recipeIngredient": [
  "3 ripe bananas, mashed",
  "1 cup sugar",
  { "@type": "PropertyValue", "value": "2", "name": "eggs" }
]
```

String format is simpler and most common.

## Instructions

`recipeInstructions` can be:

### Plain text (simple)
```json
"recipeInstructions": "Preheat oven to 350°F. Mix ingredients. Bake for 1 hour."
```

### HowToStep array (structured)
```json
"recipeInstructions": [
  {
    "@type": "HowToStep",
    "text": "Preheat oven to 350°F."
  },
  {
    "@type": "HowToStep",
    "text": "Mix dry ingredients in a large bowl."
  }
]
```

### HowToSection for grouped steps
```json
"recipeInstructions": [
  {
    "@type": "HowToSection",
    "name": "Make the dough",
    "itemListElement": [
      { "@type": "HowToStep", "text": "Combine flour and salt." },
      { "@type": "HowToStep", "text": "Add water and knead." }
    ]
  },
  {
    "@type": "HowToSection",
    "name": "Shape and bake",
    "itemListElement": [
      { "@type": "HowToStep", "text": "Divide into 8 portions." },
      { "@type": "HowToStep", "text": "Bake at 400°F for 20 minutes." }
    ]
  }
]
```

## Nutrition

Use `NutritionInformation` type:

```json
"nutrition": {
  "@type": "NutritionInformation",
  "calories": "240 calories",
  "fatContent": "9 g",
  "carbohydrateContent": "32 g",
  "proteinContent": "5 g",
  "fiberContent": "2 g",
  "sodiumContent": "200 mg"
}
```

## Dietary restrictions

`suitableForDiet` uses Schema.org URLs:

```json
"suitableForDiet": "https://schema.org/VeganDiet"
```

Available values:
- `DiabeticDiet`
- `GlutenFreeDiet`
- `HalalDiet`
- `HinduDiet`
- `KosherDiet`
- `LowCalorieDiet`
- `LowFatDiet`
- `LowLactoseDiet`
- `LowSaltDiet`
- `VeganDiet`
- `VegetarianDiet`

## Complete example

```json
{
  "@context": "https://schema.org",
  "@type": "Recipe",
  "name": "Classic Banana Bread",
  "author": "Jane Smith",
  "datePublished": "2024-01-15",
  "description": "Moist banana bread with walnuts.",
  "image": "https://example.com/banana-bread.jpg",
  "prepTime": "PT15M",
  "cookTime": "PT1H",
  "totalTime": "PT1H15M",
  "recipeYield": "1 loaf (10 slices)",
  "recipeCategory": "Dessert",
  "recipeCuisine": "American",
  "keywords": "banana, bread, baking, breakfast",
  "recipeIngredient": [
    "3 ripe bananas, mashed",
    "1/3 cup melted butter",
    "3/4 cup sugar",
    "1 egg, beaten",
    "1 teaspoon vanilla",
    "1 teaspoon baking soda",
    "1 1/2 cups all-purpose flour",
    "1/2 cup chopped walnuts"
  ],
  "recipeInstructions": [
    {
      "@type": "HowToStep",
      "text": "Preheat oven to 350°F (175°C). Grease a 9x5 inch loaf pan."
    },
    {
      "@type": "HowToStep",
      "text": "Mash bananas in a bowl. Stir in melted butter."
    },
    {
      "@type": "HowToStep",
      "text": "Mix in sugar, egg, and vanilla."
    },
    {
      "@type": "HowToStep",
      "text": "Add baking soda and flour, stirring until just combined. Fold in walnuts."
    },
    {
      "@type": "HowToStep",
      "text": "Pour into prepared pan. Bake 60-65 minutes until a toothpick comes out clean."
    }
  ],
  "nutrition": {
    "@type": "NutritionInformation",
    "calories": "240 calories",
    "fatContent": "9 g"
  },
  "suitableForDiet": "https://schema.org/VegetarianDiet"
}
```
