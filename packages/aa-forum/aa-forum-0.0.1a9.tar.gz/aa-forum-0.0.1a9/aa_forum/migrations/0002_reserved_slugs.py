from django.db import migrations

reserved_slugs_to_migrate = [
    {"slug": "admin"},
    {"slug": "administrator"},
    {"slug": "administration"},
    {"slug": "category-order"},
    {"slug": "board-order"},
]


def add_reserved_slugs(apps, schema_editor):
    """
    Add reserved slugs on migration
    :param apps:
    :type apps:
    :param schema_editor:
    :type schema_editor:
    """

    Slug = apps.get_model("aa_forum", "Slug")
    db_alias = schema_editor.connection.alias
    reserved_slugs = [
        Slug(slug=reserved_slug["slug"]) for reserved_slug in reserved_slugs_to_migrate
    ]
    Slug.objects.using(db_alias).bulk_create(reserved_slugs)


def remove_reserved_slugs(apps, schema_editor):
    """
    Remove reserved slugs on migration to zero
    :param apps:
    :type apps:
    :param schema_editor:
    :type schema_editor:
    """

    Slug = apps.get_model("aa_forum", "Slug")
    db_alias = schema_editor.connection.alias

    for reserved_slug in reserved_slugs_to_migrate:
        Slug.objects.using(db_alias).filter(slug=reserved_slug["slug"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("aa_forum", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(add_reserved_slugs, remove_reserved_slugs),
    ]
