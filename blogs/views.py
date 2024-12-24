from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, Category, Tag
from django.db.models import Count


# Helper function to fetch categories and tags for the sidebar
def get_sidebar_data():
    # 查询标签云数据
    tags = Tag.objects.annotate(count=Count('blogs'))  # 统计每个标签关联的博客数量
    max_count = max([tag.count for tag in tags], default=1)  # 获取最大计数，避免空数据报错
    sidebar_tags = [
        (tag, tag.count, 10 + (14 * tag.count // max_count))  # 动态调整字体大小
        for tag in tags
    ]

    # 查询分类数据，预取子分类
    categories = Category.objects.filter(parent_category__isnull=True).prefetch_related('subcategories')

    return categories, sidebar_tags


def blogs_list(request):
    """
    Display a paginated list of blogs with a tag cloud and categories.
    """
    # 查询博客列表
    blogs = Blog.objects.all().order_by('-published_date')
    paginator = Paginator(blogs, 9)  # 每页显示 9 篇博客
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 获取侧边栏数据
    categories, sidebar_tags = get_sidebar_data()

    # 将数据传递到模板
    context = {
        'page_obj': page_obj,
        'sidebar_tags': sidebar_tags,
        'categories': categories,  # 添加 categories 数据
    }
    return render(request, 'blogs/blogs_list.html', context)


def blog_detail(request, blog_id):
    """
    Display the details of a single blog post.
    """
    blog = get_object_or_404(Blog, pk=blog_id)

    # 获取侧边栏数据
    categories, sidebar_tags = get_sidebar_data()

    return render(request, 'blogs/detail.html', {
        'blog': blog,
        'categories': categories,
        'sidebar_tags': sidebar_tags,
    })


def category_detail(request, slug):
    """
    Display blogs belonging to a specific category and its subcategories.
    """
    category = get_object_or_404(Category, slug=slug)
    blogs = category.get_all_blogs().order_by('-published_date')
    paginator = Paginator(blogs, 9)  # 每页显示 10 篇博客
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 获取侧边栏数据
    categories, sidebar_tags = get_sidebar_data()

    return render(request, 'blogs/category_detail.html', {
        'category': category,
        'page_obj': page_obj,
        'categories': categories,
        'sidebar_tags': sidebar_tags,
    })


def tag_detail(request, slug):
    """
    Display blogs tagged with a specific tag.
    """
    tag = get_object_or_404(Tag, slug=slug)
    blogs = Blog.objects.filter(tags=tag).order_by('-published_date')
    paginator = Paginator(blogs, 9)  # 每页显示 10 篇博客
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 获取侧边栏数据
    categories, sidebar_tags = get_sidebar_data()

    return render(request, 'blogs/tag_detail.html', {
        'tag': tag,
        'page_obj': page_obj,
        'categories': categories,
        'sidebar_tags': sidebar_tags,
    })