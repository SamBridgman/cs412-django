

# Create your views here.
from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# Create your views here.

def home(request):
    '''
    Define a view to handle the 'home' request.
    '''

    response_text = '''
    <html>
    <h1>Hello, world!</h1>

    </html>
    '''
    
    return HttpResponse(response_text)
def quote(request):

    # the template to which we will delegate the work
    template = 'quotes/quote.html'

    quotes = ["“Pain is inevitable. Suffering is optional.”", "“Whatever it is you're seeking won't come in the form you're expecting.”", "“If you only read the books that everyone else is reading, you can only think what everyone else is thinking.”",
            "“Memories warm you up from the inside. But they also tear you apart.”", "“In the end, people always have to leave, don’t they? They can’t help it.”", "“Spend your money on the things money can buy. Spend your time on the things money can’t buy.”" ]
    
    image =["https://static01.nyt.com/images/2011/10/23/magazine/23murakami1_span/23murakami1_span-articleLarge.jpg",
            "https://i.guim.co.uk/img/static/sys-images/Books/Pix/pictures/2014/9/10/1410347824341/Haruki-Murakami-011.jpg?width=465&dpr=1&s=none&crop=none",
            "https://i.guim.co.uk/img/media/9d0618336a3d4b7ea3e6cec4bb8e781670c140bc/0_50_1943_2427/master/1943.jpg?width=700&quality=85&auto=format&fit=max&s=a987887882b9fa593733f3a63a4a6569",
            "https://m.media-amazon.com/images/M/MV5BNzNkYTY4YTctOTFmYi00ZDhiLTg4MTItOTkwM2I3ZjBlZDIyXkEyXkFqcGc@._V1_.jpg",
            "https://www.thewordling.com/wp-content/uploads/2022/04/haruki-murakami.jpg",
            "https://thevinylfactory.com/wp-content/uploads/2020/05/haruki-murakami-radio-show-coronavirus-lockdown.jpg"]

    # a dict of key/value pairs, to be available for use in template
    context = {
        'randomquote' : quotes[random.randint(0,5)],
        'randomimage' : image[random.randint(0,5)]
    }

    return render(request, template, context)

def show_all(request):

    # the template to which we will delegate the work
    template = 'quotes/show_all.html'

    quotes = ["“Pain is inevitable. Suffering is optional.”", "“Whatever it is you're seeking won't come in the form you're expecting.”", "“If you only read the books that everyone else is reading, you can only think what everyone else is thinking.”",
            "“Memories warm you up from the inside. But they also tear you apart.”", "“In the end, people always have to leave, don’t they? They can’t help it.”", "“Spend your money on the things money can buy. Spend your time on the things money can’t buy.”" ]
    
    image =["https://static01.nyt.com/images/2011/10/23/magazine/23murakami1_span/23murakami1_span-articleLarge.jpg",
            "https://i.guim.co.uk/img/static/sys-images/Books/Pix/pictures/2014/9/10/1410347824341/Haruki-Murakami-011.jpg?width=465&dpr=1&s=none&crop=none",
            "https://i.guim.co.uk/img/media/9d0618336a3d4b7ea3e6cec4bb8e781670c140bc/0_50_1943_2427/master/1943.jpg?width=700&quality=85&auto=format&fit=max&s=a987887882b9fa593733f3a63a4a6569",
            "https://m.media-amazon.com/images/M/MV5BNzNkYTY4YTctOTFmYi00ZDhiLTg4MTItOTkwM2I3ZjBlZDIyXkEyXkFqcGc@._V1_.jpg",
            "https://www.thewordling.com/wp-content/uploads/2022/04/haruki-murakami.jpg",
            "https://thevinylfactory.com/wp-content/uploads/2020/05/haruki-murakami-radio-show-coronavirus-lockdown.jpg"]

    # a dict of key/value pairs, to be available for use in template
    context = {
        'allquotes' : quotes,
        'allimages' : image
    }

    return render(request, template, context)

def about(request):

    # the template to which we will delegate the work
    template = 'quotes/about.html'


    # a dict of key/value pairs, to be available for use in template
    context = {
        'bio' : 'Haruki Murakami is a renowned Japanese author known for his surreal storytelling, blending magical realism with deep emotional themes. His works, including Norwegian Wood, Kafka on the Shore, and 1Q84, have captivated readers worldwide with their dreamlike narratives, introspective characters, and philosophical depth. Murakami’s writing often explores loneliness, fate, and the blurred lines between reality and imagination.',
        'mynote' : 'Hello, Im Sam Bridgman and I made this app and Im a cs major at BU.'
    }

    return render(request, template, context)

