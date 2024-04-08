from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TagForm, NoteForm
from .models import Tag, Quote


# Create your views here.
def main(request, page=1):
    quotes = Quote.objects.all().order_by('id')
    per_page = 10
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)

    return render(request, "quotes/index.html", context={"quotes": quotes_on_page, 'paginator': paginator})


@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/tag.html', {'form': form})

    return render(request, 'quotes/tag.html', {'form': TagForm()})


@login_required
def note(request):
    tags = Tag.objects.all()

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save()

            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)

            return redirect(to='quotes:main')
        else:
            return render(request, 'quotes/note.html', {"tags": tags, 'form': form})

    return render(request, 'quotes/note.html', {"tags": tags, 'form': NoteForm()})
