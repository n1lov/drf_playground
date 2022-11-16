from grappelli.dashboard import modules, Dashboard

from django.utils.translation import gettext_lazy as _


class CustomAdminDashboard(Dashboard):
    def init_with_context(self, context):
        self.children.append(modules.Group(
            title=_('Data'),
            column=1,
            collapsible=True,
            children=[
                modules.ModelList(
                    title=_('ISIN database'),
                    column=1,
                    models=(
                        'core.models.asset.IdentifiedAssetProfile',
                    )
                ),
                modules.ModelList(
                    title=_('User Assets'),
                    column=1,
                    models=(
                        'core.models.asset.Bond',
                        'core.models.asset.Stock',
                    )
                ),
                modules.ModelList(
                    title=_('Exchanges'),
                    column=1,
                    models=(
                        'core.models.exchange.Exchange',
                    )
                ),
            ]
        ))
        self.children.append(modules.RecentActions(
            'Recent activity',
            limit=5,
            collapsible=False,
            column=2
        ))
        self.children.append(modules.ModelList(
            title=_('Users administration'),
            column=1,
            models=(
                'core.models.user.User',
                # 'rest_framework.authtoken.models.Token',
                # 'django_rest_passwordreset.models.ResetPasswordToken',
            )
        ))
