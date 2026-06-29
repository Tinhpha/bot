# =====================================
# Discord AutoMod Configuration
# =====================================

# ===== Log =====

LOG_CHANNEL_ID = 1517454013904453632

# ===== Message Spam =====

MESSAGE_SPAM_LIMIT = 8          # 8 tin nhắn
MESSAGE_WINDOW = 10             # Trong 10 giây

SAME_MESSAGE_LIMIT = 5          # 5 tin giống nhau

# ===== Mention Spam =====

ROLE_MENTION_LIMIT = 3          # @Role
ROLE_WINDOW = 15

# ===== Multi Channel Spam =====

MULTI_CHANNEL_LIMIT = 3
MULTI_CHANNEL_WINDOW = 15

# ===== Voice Spam =====

VOICE_MOVE_LIMIT = 8
VOICE_WINDOW = 30

# ===== Punishment =====

MUTE_DURATION = 600             # 10 phút

DELETE_SPAM_MESSAGES = True

# ===== Ignore =====

IGNORE_OWNER = True
IGNORE_ADMIN = True
IGNORE_BOTS = True