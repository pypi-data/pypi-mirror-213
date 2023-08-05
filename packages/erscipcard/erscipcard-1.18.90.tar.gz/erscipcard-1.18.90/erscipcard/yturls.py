from django.urls import path
from . import ytviews

urlpatterns = [
    path('', ytviews.helping ),
    path('ytlink/', ytviews.vid ),
    path('shqr/', ytviews.shqr ),
    path('mp4/<str:link>/', ytviews.ytmp4 ),
    path('nginx/', ytviews.ngin ),
    path('<str:link>/', ytviews.ytdwn ),    
]
