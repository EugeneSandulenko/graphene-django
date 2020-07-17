import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType

from cookbook.ingredients.models import Category, Ingredient

# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class CategoryNode(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (graphene.Node,)
        filter_fields = ["name", "ingredients"]


class IngredientNode(DjangoObjectType):
    class Meta:
        model = Ingredient
        # Allow for some more advanced filtering here
        interfaces = (graphene.Node,)
        filter_fields = {
            "name": ["exact", "icontains", "istartswith"],
            "notes": ["exact", "icontains"],
            "category": ["exact"],
            "category__name": ["exact"],
        }


class Query(object):
    category = graphene.Node.Field(CategoryNode)
    all_categories = DjangoFilterConnectionField(CategoryNode)

    ingredient = graphene.Node.Field(IngredientNode)
    all_ingredients = DjangoFilterConnectionField(IngredientNode)


class IngredientInput(graphene.InputObjectType):
    name = graphene.String()
    notes = graphene.String()


class CreateIngredient(graphene.Mutation):
    class Arguments:
        input = IngredientInput()

    ok = graphene.Boolean()
    id = graphene.Int()
    ingredient = graphene.Field(IngredientNode)

    @staticmethod
    def mutate(root, info, input):
        category = Category.objects.get(pk=1)
        ingredient = Ingredient(name=input.name, notes=input.notes, category=category)
        ingredient.save()
        # new_ingredient = Ingredient.objects.create(ingredient)
        print(ingredient.id)
        print(input)
        print(input.notes)
        ok = True
        return CreateIngredient(id=ingredient.id, ok=ok, ingredient=ingredient)
