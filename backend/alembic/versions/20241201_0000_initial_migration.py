"""Initial migration — مرحله ۱: مدل‌های مشترک

Revision ID: 001_initial
Revises: 
Create Date: 2024-12-01 00:00:00

شامل جداول:
- users
- saved_addresses
- categories
- cities
- neighborhoods
- payments (فقط ساختار — بدون FK به bookings/orders که در مراحل بعد می‌آیند)
- favorites
- reviews (فقط ساختار)
- notifications
- reports
"""
from typing import Sequence, Union

import geoalchemy2
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """ایجاد تمام جداول مرحله ۱."""

    # فعال‌سازی extension های PostgreSQL
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis;")
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";')

    # ------------------------------------------------------------------
    # جدول cities
    # ------------------------------------------------------------------
    op.create_table(
        "cities",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("province", sa.String(length=100), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_cities_slug"), "cities", ["slug"])

    # ------------------------------------------------------------------
    # جدول neighborhoods
    # ------------------------------------------------------------------
    op.create_table(
        "neighborhoods",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("city_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["city_id"], ["cities.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_neighborhoods_city_id"), "neighborhoods", ["city_id"])

    # ------------------------------------------------------------------
    # جدول users
    # نکته: نقش کاربر از وجود رکورد ServiceProvider یا Store تشخیص داده می‌شود
    # نه از یک Enum ثابت — این طراحی از Hybrid User به‌طور طبیعی پشتیبانی می‌کند
    # ------------------------------------------------------------------
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("phone", sa.String(length=15), nullable=False),
        sa.Column("full_name", sa.String(length=100), nullable=False),
        sa.Column(
            "is_verified_identity", sa.Boolean(), server_default="false", nullable=False
        ),
        sa.Column("is_admin", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("avatar_url", sa.String(length=500), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("phone"),
    )
    op.create_index(op.f("ix_users_phone"), "users", ["phone"])

    # ------------------------------------------------------------------
    # جدول saved_addresses
    # ------------------------------------------------------------------
    op.create_table(
        "saved_addresses",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("label", sa.String(length=50), nullable=False),
        sa.Column("full_address", sa.Text(), nullable=False),
        sa.Column("lat", sa.Float(), nullable=False),
        sa.Column("lng", sa.Float(), nullable=False),
        sa.Column(
            "is_default", sa.Boolean(), server_default="false", nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_saved_addresses_user_id"), "saved_addresses", ["user_id"]
    )

    # ------------------------------------------------------------------
    # جدول categories
    # ------------------------------------------------------------------
    category_type_enum = postgresql.ENUM(
        "service", "product", "both", name="category_type_enum", create_type=True
    )
    category_type_enum.create(op.get_bind())

    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("type", sa.Enum("service", "product", "both", name="category_type_enum"), nullable=False),
        sa.Column("icon", sa.String(length=200), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["parent_id"], ["categories.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("slug"),
    )
    op.create_index(op.f("ix_categories_slug"), "categories", ["slug"])
    # ایندکس GIN trigram برای جستجوی فارسی autocomplete
    op.execute(
        "CREATE INDEX ix_categories_name_trgm ON categories USING GIN (name gin_trgm_ops);"
    )

    # ------------------------------------------------------------------
    # جدول notifications
    # ------------------------------------------------------------------
    op.create_table(
        "notifications",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.Column("title", sa.String(length=200), nullable=False),
        sa.Column("body", sa.Text(), nullable=True),
        sa.Column("data", postgresql.JSONB(), nullable=True),
        sa.Column(
            "is_read", sa.Boolean(), server_default="false", nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_notifications_user_id"), "notifications", ["user_id"]
    )
    op.create_index(
        "ix_notifications_user_unread",
        "notifications",
        ["user_id", "is_read"],
        postgresql_where=sa.text("is_read = false"),
    )

    # ------------------------------------------------------------------
    # جدول reports
    # ------------------------------------------------------------------
    op.create_table(
        "reports",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("reporter_id", sa.Integer(), nullable=False),
        sa.Column("target_type", sa.String(length=50), nullable=False),
        sa.Column("target_id", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(length=100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column(
            "status",
            sa.String(length=20),
            server_default="pending",
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("NOW()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["reporter_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """حذف تمام جداول مرحله ۱."""
    op.drop_table("reports")
    op.drop_table("notifications")
    op.execute("DROP INDEX IF EXISTS ix_categories_name_trgm;")
    op.drop_table("categories")
    op.execute("DROP TYPE IF EXISTS category_type_enum;")
    op.drop_table("saved_addresses")
    op.drop_table("users")
    op.drop_table("neighborhoods")
    op.drop_table("cities")
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp";')
    op.execute("DROP EXTENSION IF EXISTS pg_trgm;")
    op.execute("DROP EXTENSION IF EXISTS postgis;")
