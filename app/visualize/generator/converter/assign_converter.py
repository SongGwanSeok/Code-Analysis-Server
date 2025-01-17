from app.visualize.analysis.stmt.models.assign_stmt_obj import AssignStmtObj
from app.visualize.generator.highlight.expr_highlight import ExprHighlight
from app.visualize.generator.highlight.list_highlight import ListHighlight
from app.visualize.generator.models.assign_viz import AssignViz
from app.visualize.generator.models.variable_vlz import Variable
from app.visualize.generator.visualization_manager import VisualizationManager
from app.visualize.utils import utils


class AssignConverter:
    @staticmethod
    def convert(assign_obj: AssignStmtObj, viz_manager: VisualizationManager):
        depth = viz_manager.get_depth()
        expr_stmt_obj = assign_obj.expr_stmt_obj
        var_type = utils.get_var_type(expr_stmt_obj.value, expr_stmt_obj.expr_type)
        highlights = AssignConverter._get_highlights(expr_stmt_obj, var_type)

        return AssignConverter._convert_to_assign_viz(expr_stmt_obj, assign_obj.targets, depth, highlights, var_type)

    @staticmethod
    def _get_highlights(expr_stmt_obj, var_type):
        if var_type == "variable":
            return ExprHighlight.get_highlight_indexes(expr_stmt_obj.expressions)
        elif var_type in ("list", "tuple"):
            return ListHighlight.get_highlight_indexes(expr_stmt_obj.expressions)

    @staticmethod
    def _convert_to_assign_viz(expr_stmt_obj, targets, depth, highlights, var_type):
        variable_list = [
            Variable(
                id=expr_stmt_obj.id,
                depth=depth,
                expr=expr_stmt_obj.expressions[-1],
                highlights=highlights[-1],
                name=target,
                type=var_type,
            )
            for target in targets
        ]

        return AssignViz(variables=variable_list)

    @staticmethod
    def _get_var_type(var_type: str):
        if var_type in ("name", "constant", "binop"):
            var_type = "variable"

        return var_type
