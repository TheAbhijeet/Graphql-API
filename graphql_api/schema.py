import graphene
import api.schema
# import api.relay
import graphql_jwt
# from graphql_jwt.decorators import login_required

class Query(api.schema.Query, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(api.schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)

# class Query(
#     # users.schema.Query,
#     posts.schema.Query,
#     posts.schema_relay.RelayQuery,
#     graphene.ObjectType,
# ):
#     pass