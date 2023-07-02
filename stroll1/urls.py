
from django.urls import path

from django.contrib.auth import views as auth_views

from . import views






urlpatterns = [
    path("", views.index, name="home"),
    path("custom", views.custom, name="custom"),
    path("<dest_id>/payment", views.payment, name="payment"),
    path("payment1", views.payment1, name="payment1"),
    path("search", views.search, name="search"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("register", views.register, name="register"),
    path("userpage", views.userPage, name="userpage"),
    path("<dest_id>/rating", views.ratingPage, name="rating"),             
    
    path("<dest_id>/destination_details", views.destination_details, name="destination_details"),             
    path("maps/", views.maps, name="maps"),
    path("ktm/", views.mapsktm, name="mapsktm"),
    path("bkt/", views.mapsbkt, name="mapsbkt"),
    path("lpr/", views.mapslpr, name="mapslpr"),
    path("boudha/", views.mapsboudha, name="mapsboudha"),
    path("products/", views.products, name="products"),
    path("update_item/", views.update_item, name="update_item"),
    path("cart/", views.cart, name="cart"),
    path("viewPage/", views.viewPage, name="viewPage"),
    path("processorder", views.processOrder, name="processorder"),
    path("feedback", views.feedback, name="feedback"),

    # review-update
    path('<review_id>/update_review/<dest_id>', views.update_review, name="update_review"),
    path('<review_id>/delete_review/<dest_id>', views.delete_review, name="delete_review"),

    # user profile
    path("user-profile", views.UserProfile, name="user-profile"),
    path("<order_id>/showOrderitems", views.showOrderitems, name="showOrderitems"),

    path("cash on delivery-request", views.cashondelivery, name="cashondelivery"),
    path("submit_order", views.submit_order, name="submit_order"),

    # for destination order_khalti
    path("khalti-request", views.KhaltiRequest, name="khalti-request"),
    path("khalti-verify", views.KhaltiVerify, name="khalti-verify"),

    # for destination order_khalti
    path("esewa-request", views.EsewaRequest, name="esewa-request"),
    # path("esewa-verify", views.EsewaVerify, name="esewa-verify"),

    # for cart order
    path("khalti-request-cart", views.KhaltiRequestCart, name="khalti-request-cart"),
    path("khalti-verify-cart", views.KhaltiVerifyCart, name="khalti-verify-cart"),

    #pasword-reset email
    path("reset-password", auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name="reset_password"),
    path("reset-password-sent", auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name="password_reset_done"),
    path("reset/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'),name="password_reset_confirm"),
    path("reset-password-complete", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name="password_reset_complete"),


]