from transfer import GoosyTransfer

goosy = GoosyTransfer()

local = '/data/news/csf_hot_news/20160408/h_20160408094600_b0f255673c383d48156d7ee5aa46fa8e.txt'
remote = '/data/news/test/'
goosy.put(local, remote)



