# -*- coding=utf-8 -*-

import Util
import urllib


class ThreadDeco(object):

	def __init__(self,func):
		self._func = func

	def __call__(self,*args):
		self._func(*args)
		# proxy = Proxy()
		while True:
			if not args[0].empty():
				page = args[0].get()
				if page == Util.ENG_FLAG:
					args[1].put(Util.ENG_FLAG)
					break
					
				while True:
					try:
						res = args[2].get(url=page,headers=Util.Default_Headers,timeout=2)
						status_code = res.status_code
						if status_code == 200:
							args[1].put(res)
							args[0].task_done()
							break
						elif status_code == 404:
							break
						elif status_code == 401 or status_code == 410:
							break
						# else:
						# 	Util.PROXIES['https'] = proxy.archieve_activity_proxy()
					except Exception as e:
						pass
						# Util.PROXIES['https'] = proxy.archieve_activity_proxy()
				

def init_thread(url,pageCount,url_queue,s):
	ftype = url.split('/')[-1]
	offset,count_page = 1,0
	post_data = {'offset':offset,'limit':pageCount,'include':choose_include(ftype)}
	answer_data = urllib.parse.urlencode(post_data)
	proxy = Proxy()
	while True:	
		try:
			r = s.get(url='{}?{}'.format(url,answer_data),headers=Util.Default_Headers,timeout=2)
			status_code = r.status_code
			if status_code == 200:
				count_page = (int(r.json()['paging']['totals'])-1)//pageCount + 1
				for page in range(0,count_page):
					post_data['offset'] = page*pageCount
					answer_data = urllib.parse.urlencode(post_data)
					url_queue.put('{}?{}'.format(url,answer_data))
				break
			elif status_code == 404:
				break
			elif status_code == 401 or status_code == 410:
				break
			# else:
			# 	Util.PROXIES['https'] = proxy.archieve_activity_proxy()
		except Exception as e:
			pass
			# Util.PROXIES['https'] = proxy.archieve_activity_proxy()

def choose_include(ftype):
	if ftype == 'voters':
		return 'data[*].answer_count,articles_count,follower_count,gender,is_followed,is_following,badge[?(type=best_answerer)].topics'
	elif ftype == 'followees' or ftype == 'followers':
		return 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
	elif ftype == 'favlists':
		return 'data[*].updated_time,answer_count,follower_count,creator,is_following'
	elif ftype == 'answers':
		return 'data[*].is_normal,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,mark_infos,created_time,updated_time,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp,upvoted_followees;data[*].author.badge[?(type=best_answerer)].topics'
	elif ftype == 'following-columns':
		return 'data[*].intro,followers,articles_count,image_url,image_width,image_height,is_following,last_article.created'
	elif ftype == 'following-questions' or ftype == 'questions':
		return 'data[*].created,answer_count,follower_count,author'
	elif ftype == 'comments':
		return 'data[*].author,collapsed,reply_to_author,disliked,content,voting,vote_count,is_parent_author,is_author'
	else:
		return ''

@ThreadDeco
def thread_queue(urlqueue,htmlqueue,session):
	pass