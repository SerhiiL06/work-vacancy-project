from django.core.exceptions import PermissionDenied

from .models import Vacancy
from .serializers import StatisticSerializer


def generate_statistic():
    query = "SELECT 1 as id, ROUND(AVG(calary::int), 2) as avg_calary FROM vacancies_vacancy"
    query_by_category = """SELECT  1 as id, companies_scoreofactivity.title as title, 
                            ROUND(AVG(calary::int), 2) as avg_calary FROM vacancies_vacancy
                            JOIN companies_scoreofactivity ON companies_scoreofactivity.id=vacancies_vacancy.activity_scope_id
                            GROUP BY vacancies_vacancy.activity_scope_id, companies_scoreofactivity.title"""

    calary = Vacancy.objects.raw(query)
    calary_by_category = Vacancy.objects.raw(query_by_category)
    category_data = [
        {"title": item.title, "by_category": item.avg_calary}
        for item in calary_by_category
    ]
    data = {"avg_calary": calary[0].avg_calary, "category": category_data}
    statistic_serializer = StatisticSerializer(data)
    return statistic_serializer.data


def check_respond_permission(user, vacancy_id):
    current = Vacancy.objects.get(id=vacancy_id)
    if current.company.owner != user:
        raise PermissionDenied()
