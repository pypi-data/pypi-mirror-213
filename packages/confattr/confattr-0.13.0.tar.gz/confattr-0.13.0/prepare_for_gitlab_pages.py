#!/usr/bin/env python3

import os
import shutil
import subprocess
import re

HTML = 'docs/build/html'
ARTIFACT = 'public'
LATEST = 'latest'


def get_tags() -> 'list[str]':
	return subprocess.run(['git', 'tag', '--sort=version:refname'], capture_output=True, text=True).stdout.rstrip().splitlines()

def is_tracked_by_git(path: str) -> bool:
	cmd = ['git', 'ls-files', '--error-unmatch', path]
	p = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
	return p.returncode == 0

def export_html(tag: str) -> bool:
	subprocess.run(['git', 'checkout', tag])
	if os.path.isdir(HTML) and is_tracked_by_git(HTML):
		shutil.copytree(HTML, os.path.join(ARTIFACT, tag))
		return True
	else:
		print('no HTML documentation found in %s' % tag)
		return False

def create_latest(last_tag: str) -> None:
	src = os.path.join(ARTIFACT, last_tag)
	dst = os.path.join(ARTIFACT, LATEST)
	shutil.copytree(src, dst)

def inject_links_to_other_versions(versions: 'list[str]', this_version: str) -> None:
	fn = os.path.join(ARTIFACT, this_version, 'index.html')
	with open(fn, 'rt') as f:
		html = f.read()

	SECTION_NAME = 'Versions'
	HEADING_LEVEL = 2
	if f'<h{HEADING_LEVEL}>' not in html:
		HEADING_LEVEL = 1
	HEADING_TAG_OPEN  = f'<h{HEADING_LEVEL}>'
	HEADING_TAG_CLOSE = f'</h{HEADING_LEVEL}>'
	INSERT_AFTER = '</section>'
	PATTERN_BEGIN = '''\
<section id="{section}">
{HEADING_TAG_OPEN}{Section}<a class="headerlink" href="#{section}" title="Permalink to this heading">¶</a>{HEADING_TAG_CLOSE}

<p>
This project uses <a class="reference external" href="https://semver.org/">semantic versioning</a>.
The differences between the different versions are documented in the <a class="reference external" href="{change_log}">tag descriptions</a>.
</p>

<div class="toctree-wrapper compound">
<ul>\
'''
	PATTERN_BODY = '<li class="toctree-l1">{version}</li>'
	PATTERN_END = '''\
</ul>
</div>
</section>\
'''
	PATTERN_OTHER_VERSION = '<a class="reference internal" href="{target}">{version}</a>'
	PATTERN_THIS_VERSION = '{version}'
	PATTERN_LATEST = '{version} / {latest}'

	i = html.rindex(HEADING_TAG_CLOSE)
	i = html.index(INSERT_AFTER, i)

	html_begin = html[:i]
	html_end = html[i:]

	out = [
		html_begin,
		PATTERN_BEGIN.format(Section=SECTION_NAME, section=SECTION_NAME.lower(), change_log=get_change_log(), HEADING_TAG_OPEN=HEADING_TAG_OPEN, HEADING_TAG_CLOSE=HEADING_TAG_CLOSE),
	]

	for v in reversed(versions):
		p = PATTERN_THIS_VERSION if v == this_version else PATTERN_OTHER_VERSION
		target = '../%s/index.html' % v
		item = p.format(version=v, target=target)

		if v == versions[-1]:
			v = LATEST
			p = PATTERN_THIS_VERSION if v == this_version else PATTERN_OTHER_VERSION
			target = '../%s/index.html' % v
			item = PATTERN_LATEST.format(version=item, latest=p.format(version=v, target=target))

		out.append(PATTERN_BODY.format(version=item))

	out.append(PATTERN_END)
	out.append(html_end)

	with open(fn, 'wt') as f:
		for block in out:
			f.write(block)
			f.write('\n')

def get_change_log() -> str:
	return get_project_url('change')

def get_project_url(name_start: str) -> str:
	# I cannot use tomllib yet because it requires python 3.11
	# and using non-standard libraries is not worth the effort
	reo_group = re.compile(r'\[(?P<name>[^]]+)\]')
	reo_setting = re.compile(r'''["']?(?P<key>[^'"=]+)["']?\s*=\s*["']?(?P<val>[^'"]+)["']?''')
	in_urls_section = False

	with open('pyproject.toml', 'rt') as f:
		for ln in f.readlines():
			m = reo_group.match(ln)
			if m:
				in_urls_section = m.group('name') == 'project.urls'
				continue

			m = reo_setting.match(ln)
			if m and m.group('key').strip().lower().startswith(name_start):
				return m.group('val')

	raise ValueError(f'No project URL starting with {name_start} found in pyproject.toml')


def main() -> None:
	os.mkdir(ARTIFACT)
	html_versions = []
	for tag in get_tags():
		if export_html(tag):
			html_versions.append(tag)
	create_latest(html_versions[-1])

	for tag in html_versions:
		inject_links_to_other_versions(html_versions, tag)
	inject_links_to_other_versions(html_versions, LATEST)


if __name__ == '__main__':
	main()
