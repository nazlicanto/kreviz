from django.contrib import admin
from chat.models import ChatRoom, Message

# admin.site.register(ChatRoom)
# admin.site.register(Message)


class MessageInLine(admin.TabularInline):
    model = Message
    extra = 1

class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('room_name', 'interest')  # Fields to display in the list view: timestamp ve status silindi
    list_filter = ('interest',)  # Filters to apply in the sidebar #status silindi
    search_fields = ('room_name', 'interest__name')  # Fields to search
    inlines = [MessageInLine]

    def is_private(self, obj):
        # Assuming private chat rooms have a specific naming convention
        return '_' in obj.room_name
    is_private.short_description = 'Is Private'
    is_private.boolean = True

admin.site.register(ChatRoom, ChatRoomAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('chat_room', 'user', 'timestamp')  # Adjust as needed
    list_filter = ('chat_room', 'user')
    search_fields = ('chat_room__room_name', 'user__username', 'message')

admin.site.register(Message, MessageAdmin)
