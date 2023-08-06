import logging as log
from typing import Iterable

from antlr4 import CommonTokenStream, InputStream
from diogi.functions import always_a_list

from .grammar.stOTTRLexer import stOTTRLexer
from .grammar.stOTTRParser import ParserRuleContext, stOTTRParser
from .grammar.stOTTRVisitor import stOTTRVisitor as BaseVisitor
from .model import (
    Basic,
    BlankNode,
    Instance,
    Iri,
    Literal,
    Parameter,
    Patterns,
    Prefix,
    Statement,
    Template,
    Term,
    Type,
    TypedList,
    Variable,
)


# noinspection PyPep8Naming
class stOTTRVisitor(BaseVisitor):
    def __init__(self):
        pass

    @staticmethod
    def get_elements(definition: str) -> Iterable[Statement]:
        parse_tree = stOTTRVisitor._create_parse_tree(definition)
        visitor = stOTTRVisitor()
        return visitor.visit(parse_tree)

    @staticmethod
    def _create_parse_tree(definition: str) -> ParserRuleContext:
        input_stream = InputStream(definition)
        lexer = stOTTRLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = stOTTRParser(token_stream)
        return parser.stOTTRDoc()

    def aggregateResult(self, aggregate, nextResult):
        if nextResult is None:
            return aggregate

        if aggregate is None:
            return nextResult

        if isinstance(aggregate, list):
            return aggregate + [nextResult]

        return [aggregate, nextResult]

    def visitStOTTRDoc(self, ctx: stOTTRParser.StOTTRDocContext):
        log.debug(f"Visited document: {ctx.getText()}")
        for c in ctx.children:
            for node in always_a_list(self.visit(c)):
                if node is not None:
                    yield node

    def visitStatement(self, ctx):
        log.debug(f"Visited statement: {ctx.getText()}")
        template = None
        for c in always_a_list(self.visitChildren(ctx)):
            if isinstance(c, Template):
                template = c
                continue
            if isinstance(c, Patterns):
                template.add_instances(c.instances)
                continue
            if isinstance(c, Instance):
                return c
            log.warning(f"WARNING: Unsupported statement child {type(c)}")

        return template

    def visitSignature(self, ctx: stOTTRParser.SignatureContext):
        log.debug(f"Visited signature: {ctx.getText()}")
        template = None
        for c in ctx.children:
            if isinstance(c, stOTTRParser.TemplateNameContext):
                template = Template(self.visit(c))
                continue
            if isinstance(c, stOTTRParser.ParameterListContext):
                template.add_parameters(self.visit(c))
                continue
            log.warning(f"Unexpected context type {type(c)} found in signature!")

        return template

    def visitTemplateName(self, ctx: stOTTRParser.TemplateNameContext):
        log.debug(f"Visited template name: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitParameterList(self, ctx: stOTTRParser.ParameterListContext):
        log.debug(f"Visited parameter list: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitParameter(self, ctx: stOTTRParser.ParameterContext):
        log.debug(f"Visited parameter: {ctx.getText()}")
        p = Parameter(str(ctx.Variable()))
        modifiers = [str(x) for x in ctx.ParameterMode()]
        p.optional = "?" in modifiers
        p.nonblank = "!" in modifiers
        for c in always_a_list(self.visitChildren(ctx)):
            if isinstance(c, Type):
                p.type_ = c
                continue
            p.default_value = c

        return p

    def visitDefaultValue(self, ctx: stOTTRParser.DefaultValueContext):
        log.debug(f"Visited default value: {ctx.getText()}")
        print("DEFAULT VALUE")
        result = self.visitChildren(ctx)
        print(result)
        return result

    def visitAnnotationList(self, ctx: stOTTRParser.AnnotationListContext):
        log.debug(f"Visited annotation list: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitAnnotation(self, ctx: stOTTRParser.AnnotationContext):
        log.debug(f"Visited annotation: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitBaseTemplate(self, ctx: stOTTRParser.BaseTemplateContext):
        log.debug(f"Visited base template : {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitTemplate(self, ctx: stOTTRParser.TemplateContext):
        log.debug(f"Visited template: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitPatternList(self, ctx: stOTTRParser.PatternListContext):
        log.debug(f"Visited pattern list: {ctx.getText()}")
        return Patterns(self.visitChildren(ctx))

    def visitInstance(self, ctx: stOTTRParser.InstanceContext):
        log.debug(f"Visited instance: {ctx.getText()}")
        line = ctx.start.line
        instance = Instance(self.visit(ctx.templateName()), line)

        if ctx.ListExpander():
            log.warning("ListExpander is not implmented in visitInstance")

        for argument in always_a_list(self.visit(ctx.argumentList())):
            if argument is not None:
                instance.add_argument(argument)
        return instance

    def visitArgumentList(self, ctx: stOTTRParser.ArgumentListContext):
        log.debug(f"Visited argument list: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitArgument(self, ctx: stOTTRParser.ArgumentContext):
        log.debug(f"Visited argument: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitType(self, ctx: stOTTRParser.TypeContext):
        log.debug(f"Visited type: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitListType(self, ctx: stOTTRParser.ListTypeContext):
        log.debug(f"Visited list type: {ctx.getText()}")
        return TypedList(self.visit(ctx.type_()))

    def visitNeListType(self, ctx: stOTTRParser.NeListTypeContext):
        log.debug(f"Visited NeListType: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitLubType(self, ctx: stOTTRParser.LubTypeContext):
        log.debug(f"Visited LubType: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitBasicType(self, ctx: stOTTRParser.BasicTypeContext):
        log.debug(f"Visited basic type: {ctx.getText()}")
        return Basic(ctx.getText())

    def visitTerm(self, ctx: stOTTRParser.TermContext):
        log.debug(f"Visited term {ctx.getText()}")
        text = ctx.getText()
        if text[0:1] == "?":
            return Variable(text)
        return Term(text)

    def visitConstantTerm(self, ctx: stOTTRParser.ConstantTermContext):
        log.debug(f"Visited constant term: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitConstant(self, ctx: stOTTRParser.ConstantContext):
        log.debug(f"Visited constant: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitNone(self, ctx: stOTTRParser.NoneContext):
        log.debug(f"Visited none: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitTermList(self, ctx: stOTTRParser.TermListContext):
        log.debug(f"Visited term list: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitConstantList(self, ctx: stOTTRParser.ConstantListContext):
        log.debug(f"Visited constant list: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitTurtleDoc(self, ctx: stOTTRParser.TurtleDocContext):
        log.debug(f"Visited turtle doc: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitDirective(self, ctx: stOTTRParser.DirectiveContext):
        log.debug(f"Visited directive: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitPrefixID(self, ctx: stOTTRParser.PrefixIDContext):
        log.debug(f"Visited prefix ID: {ctx.getText()}")
        return Prefix(ctx.PNAME_NS(), ctx.IRIREF())

    def visitBase(self, ctx: stOTTRParser.BaseContext):
        log.debug(f"Visited base: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitSparqlBase(self, ctx: stOTTRParser.SparqlBaseContext):
        log.debug(f"Visited SPARQL base: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitSparqlPrefix(self, ctx: stOTTRParser.SparqlPrefixContext):
        log.debug(f"Visited SPARQL prefix: {ctx.getText()}")
        return Prefix(ctx.PNAME_NS(), ctx.IRIREF())

    def visitLiteral(self, ctx: stOTTRParser.LiteralContext):
        log.debug(f"Visited literal: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitNumericLiteral(self, ctx: stOTTRParser.NumericLiteralContext):
        log.debug(f"Visited numeric literal: {ctx.getText()}")
        number = ctx.getText()
        if number.isdigit():
            return Literal(int(number))
        else:
            return Literal(float(number))

    def visitRdfLiteral(self, ctx: stOTTRParser.RdfLiteralContext):
        log.debug(f"Visited rdf literal: {ctx.getText()}")
        return Literal(ctx.getText()[1:-1])

    def visitIri(self, ctx: stOTTRParser.IriContext):
        log.debug(f"Visited IRI: {ctx.getText()}")
        return Iri(ctx.getText())

    def visitPrefixedName(self, ctx: stOTTRParser.PrefixedNameContext):
        log.debug(f"Visited prefixed name: {ctx.getText()}")
        return self.visitChildren(ctx)

    def visitBlankNode(self, ctx: stOTTRParser.BlankNodeContext):
        log.debug(f"Visited blank node: {ctx.getText()}")
        return BlankNode()

    def visitAnon(self, ctx: stOTTRParser.AnonContext):
        log.debug(f"Visited anon: {ctx.getText()}")
        return self.visitChildren(ctx)
