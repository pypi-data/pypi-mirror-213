# Generated from Turtle.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .TurtleParser import TurtleParser
else:
    from TurtleParser import TurtleParser

# This class defines a complete generic visitor for a parse tree produced by TurtleParser.

class TurtleVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TurtleParser#turtleDoc.
    def visitTurtleDoc(self, ctx:TurtleParser.TurtleDocContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TurtleParser#directive.
    def visitDirective(self, ctx:TurtleParser.DirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TurtleParser#prefixID.
    def visitPrefixID(self, ctx:TurtleParser.PrefixIDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TurtleParser#base.
    def visitBase(self, ctx:TurtleParser.BaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TurtleParser#sparqlBase.
    def visitSparqlBase(self, ctx:TurtleParser.SparqlBaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TurtleParser#sparqlPrefix.
    def visitSparqlPrefix(self, ctx:TurtleParser.SparqlPrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TurtleParser#literal.
    def visitLiteral(self, ctx:TurtleParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TurtleParser#numericLiteral.
    def visitNumericLiteral(self, ctx:TurtleParser.NumericLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TurtleParser#rdfLiteral.
    def visitRdfLiteral(self, ctx:TurtleParser.RdfLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TurtleParser#iri.
    def visitIri(self, ctx:TurtleParser.IriContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TurtleParser#prefixedName.
    def visitPrefixedName(self, ctx:TurtleParser.PrefixedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TurtleParser#blankNode.
    def visitBlankNode(self, ctx:TurtleParser.BlankNodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TurtleParser#anon.
    def visitAnon(self, ctx:TurtleParser.AnonContext):
        return self.visitChildren(ctx)



del TurtleParser