import sys
import io
import time
import math
import requests
import tkinter as tk
import tkinter.font as tkfont
import traceback
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor
from PIL import Image, ImageTk
from g_python.gextension import Extension
from g_python.hmessage import Direction
from g_python.hpacket import HPacket

extension_info = {
    "title": "Enhanced Group Interface",
    "description": "New features to facilitate the user actions",
    "version": "1.0",
    "author": "Max"
}
ext = Extension(extension_info, sys.argv)

TRANSLATIONS = {
    "en": {
        "remove_selected": "Remove selected",
        "grant_admin": "Grant Admin",
        "revoke_admin": "Revoke Admin",
        "accept_selected": "Accept selected",
        "pending_requests": "Pending requests",
        "members": "Members",
        "administrators": "Administrators",
        "delete_all_members": "⚠️ Delete all members",
        "select_all_pending_in_group": "Select all pending in group...",
        "select_all_this_page": "Select all (this page)",
        "search": "Search",
        "search_placeholder": "Search for members...",
        "page": "Page",
        "members_found": "{count} members found",
        "joined": "Joined {date}",
    },
    "pt": {
        "remove_selected": "Remover selecionados",
        "grant_admin": "Dar Admin",
        "revoke_admin": "Remover Admin",
        "accept_selected": "Aceitar selecionados",
        "pending_requests": "Pedidos pendentes",
        "members": "Membros",
        "administrators": "Administradores",
        "delete_all_members": "⚠️ Excluir todos os membros",
        "select_all_pending_in_group": "Selecionar todos os pedidos do grupo...",
        "select_all_this_page": "Selecionar todos (esta página)",
        "search": "Buscar",
        "search_placeholder": "Buscar por membro...",
        "page": "Página",
        "members_found": "{count} membros encontrados",
        "joined": "Entrou em {date}",
    },
    "es": {
        "remove_selected": "Eliminar seleccionados",
        "grant_admin": "Dar Admin",
        "revoke_admin": "Quitar Admin",
        "accept_selected": "Aceptar seleccionados",
        "pending_requests": "Solicitudes pendientes",
        "members": "Miembros",
        "administrators": "Administradores",
        "delete_all_members": "⚠️ Eliminar todos los miembros",
        "select_all_pending_in_group": "Seleccionar todas las solicitudes...",
        "select_all_this_page": "Seleccionar todo (esta página)",
        "search": "Buscar",
        "search_placeholder": "Buscar miembros...",
        "page": "Página",
        "members_found": "{count} miembros encontrados",
        "joined": "Se unió el {date}",
    },
    "fr": {
        "remove_selected": "Retirer la sélection",
        "grant_admin": "Donner droits d'Admin",
        "revoke_admin": "Retirer droits d'Admin",
        "accept_selected": "Accepter la sélection",
        "pending_requests": "Requêtes en attente",
        "members": "Membres",
        "administrators": "Administrateurs",
        "delete_all_members": "⚠️ Retirer tous les membres",
        "select_all_pending_in_group": "Sélectionner toutes les requêtes...",
        "select_all_this_page": "Tout sélectionner (cette page)",
        "search": "Chercher",
        "search_placeholder": "Chercher des membres...",
        "page": "Page",
        "members_found": "{count} membres trouvés",
        "joined": "Rejoint le {date}",
    },
    "it": {
        "remove_selected": "Rimuovi selezionati",
        "grant_admin": "Dai Admin",
        "revoke_admin": "Rimuovi Admin",
        "accept_selected": "Accetta selezionati",
        "pending_requests": "Richieste in sospeso",
        "members": "Membri",
        "administrators": "Amministratori",
        "delete_all_members": "⚠️ Rimuovi tutti i membri",
        "select_all_pending_in_group": "Seleziona tutte le richieste...",
        "select_all_this_page": "Seleziona tutto (questa pagina)",
        "search": "Cerca",
        "search_placeholder": "Cerca membri...",
        "page": "Pagina",
        "members_found": "{count} membri trovati",
        "joined": "Iscritto il {date}",
    },
    "de": {
        "remove_selected": "Ausgewählte entfernen",
        "grant_admin": "Adminrechte geben",
        "revoke_admin": "Adminrechte entziehen",
        "accept_selected": "Ausgewählte akzeptieren",
        "pending_requests": "Ausstehende Anfragen",
        "members": "Mitglieder",
        "administrators": "Administratoren",
        "delete_all_members": "⚠️ Alle Mitglieder entfernen",
        "select_all_pending_in_group": "Alle Anfragen auswählen...",
        "select_all_this_page": "Alle auswählen (diese Seite)",
        "search": "Suchen",
        "search_placeholder": "Mitglieder suchen...",
        "page": "Seite",
        "members_found": "{count} Mitglieder gefunden",
        "joined": "Beigetreten am {date}",
    },
    "nl": {
        "remove_selected": "Verwijder geselecteerde",
        "grant_admin": "Maak Admin",
        "revoke_admin": "Verwijder Admin",
        "accept_selected": "Accepteer geselecteerde",
        "pending_requests": "Openstaande verzoeken",
        "members": "Leden",
        "administrators": "Beheerders",
        "delete_all_members": "⚠️ Verwijder alle leden",
        "select_all_pending_in_group": "Selecteer alle verzoeken...",
        "select_all_this_page": "Selecteer alles (deze pagina)",
        "search": "Zoeken",
        "search_placeholder": "Zoek leden...",
        "page": "Pagina",
        "members_found": "{count} leden gevonden",
        "joined": "Lid geworden op {date}",
    },
    "fi": {
        "remove_selected": "Poista valitut",
        "grant_admin": "Anna ylläpitäjä",
        "revoke_admin": "Poista ylläpitäjä",
        "accept_selected": "Hyväksy valitut",
        "pending_requests": "Odottavat pyynnöt",
        "members": "Jäsenet",
        "administrators": "Ylläpitäjät",
        "delete_all_members": "⚠️ Poista kaikki jäsenet",
        "select_all_pending_in_group": "Valitse kaikki pyynnöt...",
        "select_all_this_page": "Valitse kaikki (tämä sivu)",
        "search": "Hae",
        "search_placeholder": "Hae jäseniä...",
        "page": "Sivu",
        "members_found": "{count} jäsentä löytyi",
        "joined": "Liittynyt {date}",
    },
    "tr": {
        "remove_selected": "Seçilenleri sil",
        "grant_admin": "Yönetici yap",
        "revoke_admin": "Yöneticiliği al",
        "accept_selected": "Seçilenleri onayla",
        "pending_requests": "Bekleyen istekler",
        "members": "Üyeler",
        "administrators": "Yöneticiler",
        "delete_all_members": "⚠️ Tüm üyeleri sil",
        "select_all_pending_in_group": "Tüm istekleri seç...",
        "select_all_this_page": "Tümünü seç (bu sayfa)",
        "search": "Ara",
        "search_placeholder": "Üye ara...",
        "page": "Sayfa",
        "members_found": "{count} üye bulundu",
        "joined": "Katılım tarihi {date}",
    }
}

current_language = "en"

def t(key, **kwargs):
    text = TRANSLATIONS.get(current_language, TRANSLATIONS["en"]).get(key, key)
    return text.format(**kwargs) if kwargs else text

class HabboButton(tk.Canvas):
    def __init__(self, parent, text, command=None, width=120, height=24, bg_color="#E3E3E3", hover_color="#CCCCCC", font_size=9, font_weight="bold"):
        super().__init__(parent, width=width, height=height, bg="#EBEBEB", highlightthickness=0)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.font_size = font_size
        self.font_weight = font_weight
        self.text_string = text
        
        self.draw_button(bg_color)
        
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def draw_button(self, fill_color):
        self.delete("all")
        w, h = int(self['width']), int(self['height'])
        
        r = 3
        points = [
            r, 0, w-r, 0,
            w, r, w, h-r,
            w-r, h, r, h,
            0, h-r, 0, r
        ]
        
        self.create_polygon(points, fill=fill_color, outline="#000000", width=1)
        
        if fill_color != "#CCCCCC":
            self.create_line(r, 1, w-r, 1, fill="#FFFFFF")
            self.create_line(1, r, 1, h-r, fill="#FFFFFF")
            self.create_line(r, h-1, w-r, h-1, fill="#707070")
            self.create_line(w-1, r, w-1, h-1, fill="#707070")
        else:
            self.create_line(r, 1, w-r, 1, fill="#707070")
            self.create_line(1, r, 1, h-r, fill="#707070")
            self.create_line(r, h-1, w-r, h-1, fill="#FFFFFF")
            self.create_line(w-1, r, w-1, h-1, fill="#FFFFFF")

        self.text = self.create_text(w/2, h/2, text=self.text_string, font=("Ubuntu", self.font_size, self.font_weight), fill="#000000")

    def on_press(self, event):
        self.draw_button("#CCCCCC")
        self.coords(self.text, int(self['width'])/2 + 1, int(self['height'])/2 + 1)
        
    def on_release(self, event):
        self.draw_button(self.hover_color)
        self.coords(self.text, int(self['width'])/2, int(self['height'])/2)
        if self.command:
            self.command()
            
    def on_enter(self, event):
        self.draw_button(self.hover_color)
        
    def on_leave(self, event):
        self.draw_button(self.bg_color)

    def set_text(self, new_text):
        self.text_string = new_text
        font = tkfont.Font(family="Ubuntu", size=self.font_size, weight=self.font_weight)
        text_width = font.measure(new_text)
        min_width = text_width + 16
        if min_width > int(self['width']):
            self.config(width=min_width)
        self.draw_button(self.bg_color)

GUILD_MEMBERS_RESPONSE_HEADER = "GuildMembers"
REQUEST_MEMBERS_HEADER = "GetGuildMembers"
KICK_MEMBER_HEADER = "KickMember"
APPROVE_MEMBERSHIP_HEADER = "ApproveMembershipRequest"
SET_ADMIN_HEADER = "AddAdminRightsToMember"
REMOVE_ADMIN_HEADER = "RemoveAdminRightsFromMember"

MY_USERNAME = None
AVATAR_URL = "https://www.habbo.com.br/habbo-imaging/avatarimage?figure={figure}&direction=2&head_direction=2&headonly=1&size=b"
RANK_NAMES = {0: "Owner", 1: "Admin", 2: "Member", 3: "Requested"}
RANK_OWNER, RANK_ADMIN, RANK_MEMBER = 0, 1, 2
PAGE_SIZE = 14
BULK_DELAY_PER_ACTION = 0.5
BULK_DELAY_PER_PAGE = 1.0

http_session = requests.Session()
avatar_pool = ThreadPoolExecutor(max_workers=14)
current_guild_id = None
current_view = "members"
current_level_id = 0
current_query = ""
current_page = 0
current_total_results = 0
current_page_members = []
my_rank_in_current_guild = None

bulk_mode = None
bulk_processed_ids = set()
bulk_action_count = 0

avatar_bytes_cache = {}
avatar_photo_cache = {}
badge_photo_cache = {}
checkbox_vars = {}

offset_x, offset_y = 0, 0

HOTEL_CODE_TO_LANGUAGE = {
    "br": "pt",
    "es": "es",
    "fr": "fr",
    "it": "it",
    "de": "de",
    "nl": "nl",
    "fi": "fi",
    "tr": "tr",
    "com": "en"
}

def detect_language_from_host(host):
    try:
        subdomain = host.split('.')[0]
        code = subdomain.replace('game-', '')
    except Exception:
        code = ""
    return HOTEL_CODE_TO_LANGUAGE.get(code, "en")

def on_user_object(message):
    global MY_USERNAME
    packet = message.packet
    try:
        packet.read_int()
        MY_USERNAME = packet.read_string(encoding="utf-8")
        print(f"[Extension] Logged-in user identified: {MY_USERNAME}")
    except Exception as e:
        print(f"[Extension] Error reading UserObject: {e}")

def request_user_info():
    try:
        ext.send_to_server(HPacket('InfoRetrieve'))
    except Exception as e:
        print(f"[Extension] Could not request InfoRetrieve: {e}")

ext.intercept(Direction.TO_CLIENT, on_user_object, 'UserObject')

def start_drag(event):
    global offset_x, offset_y
    offset_x = event.x
    offset_y = event.y

def drag_window(event):
    x = window.winfo_x() - offset_x + event.x
    y = window.winfo_y() - offset_y + event.y
    window.geometry(f"+{x}+{y}")

def show_window():
    window.deiconify()
    window.overrideredirect(True)
    window.lift()
    window.attributes('-topmost', True)
    window.focus_force()

def hide_window():
    window.withdraw()

def update_window_header_and_counter():
    titles = {
        "members": t("members"),
        "admins": t("administrators"),
        "pending": t("pending_requests")
    }
    title_label.config(text=titles.get(current_view, t("members")))
    counter_label.config(text=t("members_found", count=current_total_results))

def on_search_in(e):
    if search_entry.get() == "Search for members...":
        search_entry.delete(0, tk.END)
        search_entry.config(fg="black")

def on_search_out(e):
    if search_entry.get() == "":
        search_entry.insert(0, "Search for members...")
        search_entry.config(fg="grey")

def do_search(event=None):
    global current_query, current_page
    val = search_entry.get()
    current_query = "" if val == "Search for members..." else val
    current_page = 0
    request_current_page()

def toggle_select_all_page():
    check_value = select_all_var.get()
    for member in current_page_members:
        if member["rank"] == RANK_OWNER:
            continue
        if current_view == "members" and member["rank"] == RANK_ADMIN:
            continue
        if member["userId"] in checkbox_vars:
            checkbox_vars[member["userId"]].set(check_value)

def clear_member_list():
    for widget in member_list_frame.winfo_children():
        widget.destroy()
    checkbox_vars.clear()

def fetch_avatar_bytes(look):
    if look in avatar_bytes_cache: return avatar_bytes_cache[look]
    try:
        response = http_session.get(AVATAR_URL.format(figure=look), timeout=5)
        avatar_bytes_cache[look] = response.content
        return response.content
    except:
        return None

def get_avatar_photo(look, avatar_bytes):
    if look in avatar_photo_cache: return avatar_photo_cache[look]
    if avatar_bytes is None: return None
    try:
        image = Image.open(io.BytesIO(avatar_bytes))
        photo = ImageTk.PhotoImage(image)
        avatar_photo_cache[look] = photo
        return photo
    except:
        return None

def build_member_row(member, row_index, col_index):
    card = tk.Canvas(member_list_frame, width=220, height=45, bg="#EBEBEB", highlightthickness=0)
    
    w, h = 220, 45
    r = 4
    points = [r, 0, w-r, 0, w, r, w, h-r, w-r, h, r, h, 0, h-r, 0, r]
    card.create_polygon(points, fill="#FFFFFF", outline="#000000", width=1)

    var = tk.BooleanVar()
    checkbox_vars[member["userId"]] = var
    chk = tk.Checkbutton(card, variable=var, bg="#FFFFFF", activebackground="#FFFFFF", highlightthickness=0)
    card.create_window(12, 22, window=chk, anchor="w")

    photo = get_avatar_photo(member["look"], member.get("avatar_bytes"))
    if photo is not None:
        card.create_image(40, 22, image=photo, anchor="w")
        
    card.create_text(100, 14, text=member["username"], font=("Ubuntu", 9, "bold"), fill="#000000", anchor="w")

    rank = member["rank"]
    if rank == RANK_OWNER:
        if img_icon_owner:
            card.create_image(100, 28, image=img_icon_owner, anchor="w")
        date_x_pos = 118
    elif rank == RANK_ADMIN:
        if img_icon_admin:
            card.create_image(100, 28, image=img_icon_admin, anchor="w")
        date_x_pos = 118
    else:
        date_x_pos = 100
    
    join_text = t("joined", date=member.get('joinDate', '')) if member.get('joinDate') else ""
    card.create_text(date_x_pos, 28, text=join_text, font=("Ubuntu", 7, "italic"), fill="#777777", anchor="w")

    card.grid(row=row_index, column=col_index, sticky="ew", padx=3, pady=3)

def render_members(members):
    global current_page_members
    current_page_members = members
    select_all_var.set(False)
    clear_member_list()
    for index, member in enumerate(members):
        build_member_row(member, index // 2, index % 2)

def total_pages():
    return max(1, math.ceil(current_total_results / PAGE_SIZE))

def update_pagination_label():
    page_entry.delete(0, tk.END)
    page_entry.insert(0, str(current_page + 1))
    page_label_total.config(text=f"/ {total_pages()}")

def next_page():
    global current_page
    if current_page < total_pages() - 1:
        current_page += 1
        update_pagination_label()
        request_current_page()

def prev_page():
    global current_page
    if current_page > 0:
        current_page -= 1
        update_pagination_label()
        request_current_page()

def on_page_enter(event):
    global current_page
    try:
        target_page = int(page_entry.get()) - 1
        if 0 <= target_page < total_pages():
            current_page = target_page
            update_pagination_label()
            request_current_page()
        else:
            update_pagination_label()
    except ValueError:
        update_pagination_label()

def request_current_page():
    if current_guild_id:
        ext.send_to_server(HPacket(REQUEST_MEMBERS_HEADER, current_guild_id, current_page, current_query, current_level_id))

def switch_view(view_name, level_id):
    global current_view, current_level_id, current_page, current_query
    current_view = view_name
    current_level_id = level_id
    current_page = 0
    current_query = ""
    search_entry.delete(0, tk.END)
    search_entry.insert(0, "Search for members...")
    search_entry.config(fg="grey")
    request_current_page()

def view_members(): switch_view("members", 0)
def view_pending(): switch_view("pending", 2)
def view_admins(): switch_view("admins", 1)

def selected_user_ids():
    return [uid for uid, var in checkbox_vars.items() if var.get()]

def kick_selected():
    for uid in selected_user_ids():
        ext.send_to_server(HPacket(KICK_MEMBER_HEADER, current_guild_id, uid, False))

def accept_selected():
    for uid in selected_user_ids():
        ext.send_to_server(HPacket(APPROVE_MEMBERSHIP_HEADER, current_guild_id, uid))

def grant_admin_selected():
    for uid in selected_user_ids():
        ext.send_to_server(HPacket(SET_ADMIN_HEADER, current_guild_id, uid))

def revoke_admin_selected():
    for uid in selected_user_ids():
        ext.send_to_server(HPacket(REMOVE_ADMIN_HEADER, current_guild_id, uid))

def start_bulk_kick_members():
    if get_effective_rank() != RANK_OWNER:
        return
    
    confirmed = messagebox.askokcancel(
        "WARNING - Critical Action",
        "YOU ARE ABOUT TO REMOVE EVERY MEMBER FROM THIS GROUP.\n\n"
        "Admins and the Owner will be kept.\n"
        "THIS CANNOT BE UNDONE.",
        icon="error"
    )
    
    if not confirmed:
        return
    begin_bulk_operation("kick_members")

def start_bulk_accept_pending():
    if get_effective_rank() != RANK_OWNER:
        return
    if messagebox.askyesno("Are you sure?", "You are about to accept every pending membership request in this group."):
        begin_bulk_operation("accept_pending")

def begin_bulk_operation(mode):
    global bulk_mode, bulk_processed_ids, bulk_action_count
    bulk_mode = mode
    bulk_processed_ids = set()
    bulk_action_count = 0
    request_bulk_page()

def request_bulk_page():
    if current_guild_id:
        level_id = 0 if bulk_mode == "kick_members" else 2
        ext.send_to_server(HPacket(REQUEST_MEMBERS_HEADER, current_guild_id, 0, "", level_id))

def handle_bulk_step(members):
    global bulk_action_count
    if not members:
        finish_bulk_operation()
        return

    made_progress = False
    for m in members:
        if m["userId"] in bulk_processed_ids: continue
        bulk_processed_ids.add(m["userId"])

        if bulk_mode == "kick_members" and m["rank"] == RANK_MEMBER:
            ext.send_to_server(HPacket(KICK_MEMBER_HEADER, current_guild_id, m["userId"], False))
        elif bulk_mode == "accept_pending":
            ext.send_to_server(HPacket(APPROVE_MEMBERSHIP_HEADER, current_guild_id, m["userId"]))
        
        bulk_action_count += 1
        made_progress = True
        time.sleep(BULK_DELAY_PER_ACTION)

    if not made_progress:
        finish_bulk_operation()
        return
    time.sleep(BULK_DELAY_PER_PAGE)
    request_bulk_page()

def finish_bulk_operation():
    global bulk_mode
    count = bulk_action_count
    action_word = "removed" if bulk_mode == "kick_members" else "accepted"
    bulk_mode = None
    window.after(0, lambda: messagebox.showinfo("Done", f"{count} members {action_word}."))
    window.after(0, view_members)

def get_effective_rank():
    return my_rank_in_current_guild if my_rank_in_current_guild is not None else RANK_MEMBER

def update_nav_buttons():
    for btn in [btn_view_members, btn_view_pending, btn_view_admins, btn_accept, btn_kick, btn_grant, btn_revoke]:
        btn.pack_forget()
    btn_delete_all_members.pack_forget()
    btn_select_all_group_pending.pack_forget()
    select_all_checkbox.pack_forget()

    effective_rank = get_effective_rank()

    visible_btns = []
    if current_view != "members": visible_btns.append(btn_view_members)
    if current_view != "pending" and effective_rank != RANK_MEMBER: visible_btns.append(btn_view_pending)
    if current_view != "admins": visible_btns.append(btn_view_admins)

    if current_view == "pending" and effective_rank in (RANK_OWNER, RANK_ADMIN):
        visible_btns.append(btn_accept)

    if effective_rank in (RANK_OWNER, RANK_ADMIN):
        if current_view == "members":
            visible_btns.extend([btn_kick, btn_grant, btn_revoke])
        elif current_view == "admins":
            visible_btns.append(btn_revoke)

    for index, btn in enumerate(visible_btns):
        target_row = row1 if index < 3 else (row2 if index < 6 else row3)
        btn.pack(in_=target_row, side="left", padx=3)

    if effective_rank == RANK_OWNER:
        select_all_checkbox.pack(side="left")
        if current_view == "members":
            btn_delete_all_members.pack(side="left", padx=10)
        elif current_view == "pending":
            btn_select_all_group_pending.pack(side="left", padx=10)

def on_get_guild_members_outgoing(message):
    global current_view, current_level_id, current_page, current_query
    p = message.packet
    try:
        p.read_int()
        page = p.read_int()
        query = p.read_string()
        level_id = p.read_int()
        
        current_page = page
        current_query = query
        current_level_id = level_id
        
        if level_id == 2:
            current_view = "pending"
        elif level_id == 1:
            current_view = "admins"
        else:
            current_view = "members"
            
        print(f"[Extension] Tab synchronized via game client: {current_view} (level_id={level_id}, page={current_page})")
    except Exception as e:
        print(f"[Extension] Error reading outgoing GetGuildMembers: {e}")

ext.intercept(Direction.TO_SERVER, on_get_guild_members_outgoing, REQUEST_MEMBERS_HEADER)

def on_guild_members(message):
    global current_guild_id, my_rank_in_current_guild, current_total_results

    p = message.packet
    message.is_blocked = False
    try:
        parsed_guild_id = p.read_int()
        if current_guild_id != parsed_guild_id:
            current_guild_id = parsed_guild_id
            my_rank_in_current_guild = None

        p.read_string(encoding="utf-8")
        p.read_int()
        badge_code = p.read_string(encoding="utf-8")
        total_results = p.read_int()
        count = p.read_int()
    except Exception as e:
        print(f"[Extension] Error reading GuildMembers header: {e}")
        traceback.print_exc()
        return

    members = []

    for i in range(count):
        try:
            rank = p.read_int()
            user_id = p.read_int()
            username = p.read_string(encoding="utf-8")
            look = p.read_string(encoding="utf-8")
            join_date = p.read_string(encoding="utf-8")
            members.append({
                "userId": user_id,
                "username": username,
                "rank": rank,
                "look": look,
                "joinDate": join_date
            })
        except Exception as e:
            print(f"[Extension] Error parsing member at index {i}: {e}")
            traceback.print_exc()
            break

    my_entry = next((m for m in members if m["username"] == MY_USERNAME), None)
    if my_entry is not None:
        my_rank_in_current_guild = my_entry["rank"]

    if bulk_mode is not None:
        handle_bulk_step(members)
        return

    current_total_results = total_results

    avatar_bytes_list = list(avatar_pool.map(lambda m: fetch_avatar_bytes(m["look"]), members))

    for member, avatar_bytes in zip(members, avatar_bytes_list):
        member["avatar_bytes"] = avatar_bytes

    try:
        if badge_code not in badge_photo_cache:
            badge_url = f"https://www.habbo.com.br/habbo-imaging/badge/{badge_code}.gif"
            badge_res = http_session.get(badge_url, timeout=3)
            badge_photo_cache[badge_code] = ImageTk.PhotoImage(Image.open(io.BytesIO(badge_res.content)))
            badge_img = badge_photo_cache[badge_code]
            badge_canvas.badge_ref = badge_img
            badge_canvas.itemconfig(badge_image_on_canvas, image=badge_img)
    except Exception as e:
        print(f"Failed to fetch badge: {e}")

    window.after(0, render_members, members)
    window.after(0, update_nav_buttons)
    window.after(0, update_pagination_label)
    window.after(0, update_window_header_and_counter)
    window.after(0, show_window)

window = tk.Tk()
window.title("Display Project")
window.configure(bg="#EBEBEB")
window.overrideredirect(True)
window.protocol("WM_DELETE_WINDOW", hide_window)

def create_horizontal_border(image_path, target_width=220, corner_w=4):
    try:
        img = Image.open(image_path).convert("RGBA")
        w, h = img.size
        left_part = img.crop((0, 0, corner_w, h))
        middle_part = img.crop((corner_w, 0, w - corner_w, h)).resize((target_width - (2 * corner_w), h), Image.NEAREST)
        right_part = img.crop((w - corner_w, 0, w, h))
        
        new_img = Image.new("RGBA", (target_width, h))
        new_img.paste(left_part, (0, 0))
        new_img.paste(middle_part, (corner_w, 0))
        new_img.paste(right_part, (target_width - corner_w, 0))
        return ImageTk.PhotoImage(new_img)
    except Exception as e:
        print(f"Error processing border asset {image_path}: {e}")
        return None

img_card_top = create_horizontal_border("images/1889_guild_color_top_1_png.png", target_width=220, corner_w=4)
img_card_btm = create_horizontal_border("images/2260_guild_color_btm_1_png.png", target_width=220, corner_w=4)

try:
    img_icon_owner = ImageTk.PhotoImage(Image.open("images/2015_icon_group_owner_1_png.png"))
    img_icon_admin = ImageTk.PhotoImage(Image.open("images/2326_icon_group_admin_1_png.png"))
except Exception as e:
    print(f"Erro ao carregar ícones de rank: {e}")
    img_icon_owner, img_icon_admin = None, None

title_bar = tk.Frame(window, bg="#367897", relief="flat", bd=0, height=28)
title_bar.pack(fill="x", side="top")
title_bar.pack_propagate(False)
title_bar.bind("<Button-1>", start_drag)
title_bar.bind("<B1-Motion>", drag_window)
title_label = tk.Label(title_bar, text="Membros", bg="#367897", fg="white", font=("Ubuntu", 9, "bold"))
title_label.pack(side="left", padx=10, expand=True)
title_label.bind("<Button-1>", start_drag)
title_label.bind("<B1-Motion>", drag_window)
close_button = tk.Button(title_bar, text="X", bg="#cc0000", fg="white", font=("Ubuntu", 8, "bold"), relief="raised", bd=1, command=hide_window)
close_button.pack(side="right", padx=3, pady=3)

header_frame = tk.Frame(window, bg="#EBEBEB")
header_frame.pack(fill="x", padx=6, pady=6)
badge_canvas = tk.Canvas(header_frame, width=50, height=50, bg="#EBEBEB", highlightthickness=0)
badge_canvas.pack(side="left", padx=(0, 10))
badge_image_on_canvas = badge_canvas.create_image(25, 25, anchor="center")

right_header = tk.Frame(header_frame, bg="#EBEBEB")
right_header.pack(side="left", fill="x", expand=True)
search_frame = tk.Frame(right_header, bg="#EBEBEB")
search_frame.pack(fill="x")
search_entry = tk.Entry(search_frame, fg="grey", font=("Ubuntu", 9))
search_entry.pack(side="left", fill="x", expand=True, ipady=2)
search_entry.insert(0, "Procurar por membro...")
search_entry.bind("<FocusIn>", on_search_in)
search_entry.bind("<FocusOut>", on_search_out)
search_entry.bind("<Return>", do_search)
search_button = HabboButton(search_frame, text="Search", command=do_search, width=60)
search_button.pack(side="left", padx=(4, 0))

select_frame = tk.Frame(right_header, bg="#EBEBEB")
select_frame.pack(fill="x", pady=(4, 0))
select_all_var = tk.BooleanVar()
select_all_checkbox = tk.Checkbutton(select_frame, text="Select all (this page)", variable=select_all_var, command=toggle_select_all_page, bg="#EBEBEB", activebackground="#EBEBEB")

btn_delete_all_members = HabboButton(select_frame, text="⚠️ Delete all members", command=start_bulk_kick_members, width=130, font_size=8,font_weight="normal")
btn_select_all_group_pending = HabboButton(select_frame, text="Select all pending in group...", command=start_bulk_accept_pending, width=200)

member_list_frame = tk.Frame(window, bg="#EBEBEB")
member_list_frame.pack(fill="both", expand=True, padx=6)
member_list_frame.columnconfigure(0, weight=1)
member_list_frame.columnconfigure(1, weight=1)

pagination_frame = tk.Frame(window, bg="#EBEBEB")
pagination_frame.pack(pady=5)
HabboButton(pagination_frame, text="◀", command=prev_page, width=40, height=24, font_size=12).pack(side="left", padx=5)
page_label = tk.Label(pagination_frame, text="Page", bg="#EBEBEB", font=("Ubuntu", 8))
page_label.pack(side="left")
page_entry = tk.Entry(pagination_frame, width=4, justify="center", font=("Ubuntu", 8))
page_entry.pack(side="left", padx=2)
page_entry.bind("<Return>", on_page_enter)
page_label_total = tk.Label(pagination_frame, text="/ 1", bg="#EBEBEB", font=("Ubuntu", 8))
page_label_total.pack(side="left", padx=(0, 5))
HabboButton(pagination_frame, text="▶", command=next_page, width=40, height=24, font_size=12).pack(side="left", padx=5)
counter_label = tk.Label(pagination_frame, text="0 members found", bg="#EBEBEB", font=("Ubuntu", 8, "italic"))
counter_label.pack(side="left", padx=(5, 10))

button_container = tk.Frame(window, bg="#EBEBEB")
button_container.pack(fill="x", pady=5)
row1 = tk.Frame(button_container, bg="#EBEBEB")
row1.pack(anchor="center", pady=2)
row2 = tk.Frame(button_container, bg="#EBEBEB")
row2.pack(anchor="center", pady=2)
row3 = tk.Frame(button_container, bg="#EBEBEB")
row3.pack(anchor="center", pady=2)

btn_kick = HabboButton(button_container, text="Remove selected", command=kick_selected)
btn_grant = HabboButton(button_container, text="Grant Admin", command=grant_admin_selected)
btn_revoke = HabboButton(button_container, text="Revoke Admin", command=revoke_admin_selected)
btn_accept = HabboButton(button_container, text="Accept selected", command=accept_selected)
btn_view_pending = HabboButton(button_container, text="Pending requests", command=view_pending, width=140)
btn_view_members = HabboButton(button_container, text="Members", command=view_members, width=100)
btn_view_admins = HabboButton(button_container, text="Administrators", command=view_admins, width=130)

update_nav_buttons()

window.update_idletasks()
window_width = window.winfo_reqwidth()
window_height = window.winfo_reqheight()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
position_x = int((screen_width / 2) - (window_width / 2))
position_y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"+{position_x}+{position_y}")
window.withdraw()

def apply_language():
    btn_kick.set_text(t("remove_selected"))
    btn_grant.set_text(t("grant_admin"))
    btn_revoke.set_text(t("revoke_admin"))
    btn_accept.set_text(t("accept_selected"))
    btn_view_pending.set_text(t("pending_requests"))
    btn_view_members.set_text(t("members"))
    btn_view_admins.set_text(t("administrators"))
    btn_delete_all_members.set_text(t("delete_all_members"))
    btn_select_all_group_pending.set_text(t("select_all_pending_in_group"))
    select_all_checkbox.config(text=t("select_all_this_page"))
    search_button.set_text(t("search"))
    page_label.config(text=t("page"))
    if search_entry.get() in (TRANSLATIONS["en"]["search_placeholder"], TRANSLATIONS["pt"]["search_placeholder"]):
        search_entry.delete(0, tk.END)
        search_entry.insert(0, t("search_placeholder"))
    update_window_header_and_counter()

ext.intercept(Direction.TO_CLIENT, on_guild_members, GUILD_MEMBERS_RESPONSE_HEADER)
def on_connection_start():
    global current_language
    print(f"[Extension] Connection info: {ext.connection_info}")
    current_language = detect_language_from_host(ext.connection_info.get('host', ''))
    print(f"[Extension] Language detected: {current_language}")
    window.after(0, apply_language)
    request_user_info()

ext.on_event('connection_start', on_connection_start)
request_user_info()

ext.start()
window.mainloop()