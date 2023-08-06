# Generated from stOTTR.g4 by ANTLR 4.13.0
from antlr4 import *
if "." in __name__:
    from .stOTTRParser import stOTTRParser
else:
    from stOTTRParser import stOTTRParser

# This class defines a complete generic visitor for a parse tree produced by stOTTRParser.

class stOTTRVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by stOTTRParser#stOTTRDoc.
    def visitStOTTRDoc(self, ctx:stOTTRParser.StOTTRDocContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#statement.
    def visitStatement(self, ctx:stOTTRParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#signature.
    def visitSignature(self, ctx:stOTTRParser.SignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#templateName.
    def visitTemplateName(self, ctx:stOTTRParser.TemplateNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#parameterList.
    def visitParameterList(self, ctx:stOTTRParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#parameter.
    def visitParameter(self, ctx:stOTTRParser.ParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#defaultValue.
    def visitDefaultValue(self, ctx:stOTTRParser.DefaultValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#annotationList.
    def visitAnnotationList(self, ctx:stOTTRParser.AnnotationListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#annotation.
    def visitAnnotation(self, ctx:stOTTRParser.AnnotationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#baseTemplate.
    def visitBaseTemplate(self, ctx:stOTTRParser.BaseTemplateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#template.
    def visitTemplate(self, ctx:stOTTRParser.TemplateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#patternList.
    def visitPatternList(self, ctx:stOTTRParser.PatternListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#instance.
    def visitInstance(self, ctx:stOTTRParser.InstanceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#argumentList.
    def visitArgumentList(self, ctx:stOTTRParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#argument.
    def visitArgument(self, ctx:stOTTRParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#type.
    def visitType(self, ctx:stOTTRParser.TypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#listType.
    def visitListType(self, ctx:stOTTRParser.ListTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#neListType.
    def visitNeListType(self, ctx:stOTTRParser.NeListTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#lubType.
    def visitLubType(self, ctx:stOTTRParser.LubTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#basicType.
    def visitBasicType(self, ctx:stOTTRParser.BasicTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#term.
    def visitTerm(self, ctx:stOTTRParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#constantTerm.
    def visitConstantTerm(self, ctx:stOTTRParser.ConstantTermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#constant.
    def visitConstant(self, ctx:stOTTRParser.ConstantContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#none.
    def visitNone(self, ctx:stOTTRParser.NoneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#termList.
    def visitTermList(self, ctx:stOTTRParser.TermListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#constantList.
    def visitConstantList(self, ctx:stOTTRParser.ConstantListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#turtleDoc.
    def visitTurtleDoc(self, ctx:stOTTRParser.TurtleDocContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#directive.
    def visitDirective(self, ctx:stOTTRParser.DirectiveContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#prefixID.
    def visitPrefixID(self, ctx:stOTTRParser.PrefixIDContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#base.
    def visitBase(self, ctx:stOTTRParser.BaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#sparqlBase.
    def visitSparqlBase(self, ctx:stOTTRParser.SparqlBaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#sparqlPrefix.
    def visitSparqlPrefix(self, ctx:stOTTRParser.SparqlPrefixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#literal.
    def visitLiteral(self, ctx:stOTTRParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#numericLiteral.
    def visitNumericLiteral(self, ctx:stOTTRParser.NumericLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#rdfLiteral.
    def visitRdfLiteral(self, ctx:stOTTRParser.RdfLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#iri.
    def visitIri(self, ctx:stOTTRParser.IriContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#prefixedName.
    def visitPrefixedName(self, ctx:stOTTRParser.PrefixedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#blankNode.
    def visitBlankNode(self, ctx:stOTTRParser.BlankNodeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by stOTTRParser#anon.
    def visitAnon(self, ctx:stOTTRParser.AnonContext):
        return self.visitChildren(ctx)



del stOTTRParser