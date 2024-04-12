from graphql.type import GraphQLSchema, GraphQLObjectType, GraphQLField, GraphQLString


class DisableIntrospectionMiddleware:
    """
    This class hides the introspection.
    """

    def resolve(next, root, info, **kwargs):
        if info.field_name.lower() in ['__schema', '_introspection']:
            query = GraphQLObjectType(
                "Query", lambda: {"Hello": GraphQLField(GraphQLString, resolver=lambda *_: "World")}
            )
            info.schema = GraphQLSchema(query=query)
            return next(root, info, **kwargs)
        return next(root, info, **kwargs)
