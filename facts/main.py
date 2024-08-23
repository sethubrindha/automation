from video_generator import Generate_video


def Run():
	try:
		generator = Generate_video()
		generator.start_crome()
		# generator.invideo_ai_login()
		# for i in range(6):
		# 	generator.generate_video()
		# 	generator.edit_video()
		# 	generator.upload_video()
		# 	break
		# generator.delete_invideo_ai_login()
		# generator.close_crome()
		# is_exported = False
		# while is_exported == True:
		# 	is_exported = generator.export_video()
		# generator.edit_video()
		# generator.upload_video()
	except Exception as e:
		print("logged out with errors \n",e)
		generator.close_crome()


Run()