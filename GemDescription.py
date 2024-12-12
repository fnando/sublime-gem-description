import sublime
import sublime_plugin
import re
import urllib
import os
import tempfile
import urllib
import json
from urllib.request import urlopen
import webbrowser
import subprocess
from pathlib import Path

from .format_text import format_text


def settings(key):
    return sublime.load_settings("Gem Description.sublime-settings").get(key)


def debug(*args):
    if settings("debug"):
        print("[gem-description]", *args)


def cache_path(gem_name):
    return os.path.join(tempfile.gettempdir(), gem_name + ".gem-info")


def has_cache(gem_name):
    return os.path.isfile(cache_path(gem_name))


def read_cache(gem_name):
    with open(cache_path(gem_name)) as file:
        return json.load(file)


def write_cache(gem_name, info):
    with open(cache_path(gem_name), "w") as file:
        file.writelines(json.dumps(info))


def fetch_gem_info(gem_name):
    bin = os.path.expanduser(settings("command"))

    command = [
        bin, "-r", "json", "-e",
        "gem '%s'; spec = Gem.loaded_specs['%s']; puts JSON.dump(summary: spec.summary, url: spec.homepage || 'https://rubygems.org/gems/%s')"
        % (gem_name, gem_name, gem_name)
    ]

    with subprocess.Popen(command,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          cwd=os.getcwd(),
                          universal_newlines=True) as result:

        result.wait()

        stdout = result.stdout.read()

        debug("stdout:", stdout)
        debug("exit code:", result.returncode)
        debug("stderr:", result.stderr.read())

        if result.returncode == 0:
            return json.loads(stdout)
        else:
            return None


def get_gem_info(gem_name):
    if has_cache(gem_name):
        info = read_cache(gem_name)
    else:
        info = fetch_gem_info(gem_name)

        if info:
            write_cache(gem_name, info)

    return info


class InsertGemDescriptionCommand(sublime_plugin.TextCommand):

    def run(self, edit, row=None, description=None, url=None):
        column_size = min(
            sublime.active_window().active_view().settings().get("rulers"))

        view = sublime.active_window().active_view()
        point = view.text_point(row, 0)
        current_line = view.substr(view.line(point))
        current_line = re.sub(r"\r?\n", " ", current_line)
        indent = re.sub(r"^(\s*).*?$", "\\1", current_line) or ""

        summary = format_text(description,
                              column_size=column_size,
                              indent=indent)

        replacement = summary

        if url != None:
            replacement += "\n" + indent + "# [" + url + "]"

        replacement += "\n" + current_line

        view.replace(edit, view.line(point), replacement)

    def is_visible(self):
        return False


class GemDescription(sublime_plugin.EventListener):

    def on_hover(self, view, point, hover_zone):
        enabled = view.match_selector(point, "source.ruby")

        debug("is enabled?", enabled)

        if not enabled:
            return

        row, col = view.rowcol(point)
        line_text = view.substr(view.line(point)).strip()
        regex = r"^gem(?:\s+[\"'](.*?)[\"']|\([\"'](.*?)[\"']\))"
        matches = re.match(regex, line_text)

        if not matches:
            debug("no matches, skip.")
            return

        gem_name = matches[1]
        debug("getting info for", gem_name)
        debug("cache path is", cache_path(gem_name))

        gem_info = get_gem_info(gem_name)

        if not gem_info:
            debug("unable to fetch gem_info")
            return

        params = {"description": gem_info["summary"], "url": gem_info["url"]}

        html = gem_info["summary"]
        html += "<br><br>"
        html += '<a href="annotate:' + gem_name + ':' + str(
            row) + '">Annotate</a>'

        if gem_info["url"] != None:
            html += ' | <a href="details:' + gem_name + ':' + str(
                row) + '">Details</a>'

        html = "<div>" + html + "</div>"

        view.show_popup(html,
                        flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                        location=point,
                        on_navigate=self.handle_navigate,
                        max_width=700)

    def handle_navigate(self, path):
        action, gem_name, row = path.split(":")
        gem_info = get_gem_info(gem_name)
        row = int(row)

        point = sublime.active_window().active_view().text_point(row, 0)

        debug(gem_info)

        if action == "details":
            webbrowser.open_new_tab(gem_info["url"])
        elif action == "annotate":
            sublime.active_window().active_view().run_command(
                "insert_gem_description", {
                    "row": row,
                    "description": gem_info["summary"],
                    "url": gem_info["url"]
                })
