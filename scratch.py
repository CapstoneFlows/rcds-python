def writeCSVFile(self):
        try:
            with open(self.dir+self.winunix+"scraped_headers.csv",'wb') as csvfile:
                csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')
                csvwriter.writerow(self.columns)
                for entry in self.itemlist:
                    row = []
                    row.append(entry[0].split('                         ')[1])
                    row.append(entry[1].string)
                    row.append(entry[2].string.split("Retail ")[1])
                    h = re.search('.*(?= x)', entry[3].string)
                    if h:
                        height = h.group(0)
                        if re.search('\d* \d/\d', height):
                            whole = height.split(" ")[0]
                            fraction = height.split(" ")[1]
                            num = fraction.split("/")[0]
                            den = fraction.split("/")[1]
                            height = str(float(whole)+float(num)/float(den))
                        w = re.search('(?<=x ).*', entry[3].string)
                        width = w.group(0)
                        if re.search('\d* \d/\d', width):
                            width = re.search('\d* \d/\d', width)
                            width = width.group(0)
                            whole = width.split(" ")[0]
                            fraction = width.split(" ")[1]
                            num = fraction.split("/")[0]
                            den = fraction.split("/")[1]
                            width = str(float(whole)+float(num)/float(den))
                    elif re.search('\d(?= \d \d/\d)', entry[3].string):
                        h = re.search('.*(?= \d \d/\d)', entry[3].string)
                        height = h.group(0)
                        if re.search('\d* \d/\d', height):
                            whole = height.split(" ")[0]
                            fraction = height.split(" ")[1]
                            num = fraction.split("/")[0]
                            den = fraction.split("/")[1]
                            height = str(float(whole)+float(num)/float(den))
                        w = re.search('(?<=\d )\d* \d/\d', entry[3].string)
                        width = w.group(0)
                        if re.search('\d* \d/\d', width):
                            width = re.search('\d* \d/\d', width)
                            width = width.group(0)
                            whole = width.split(" ")[0]
                            fraction = width.split(" ")[1]
                            num = fraction.split("/")[0]
                            den = fraction.split("/")[1]
                            width = str(float(whole)+float(num)/float(den))
                    row.append(height)
                    row.append(width)
                    row.append(entry[4].string)
                    row.append(entry[5])
                    row.append(entry[6])
                    row.append('http://www.teleky.com'+entry[7].split('..')[1])
                    self.writerow(row, csvwriter, queue, encoder, csvfile)
        except Exception as E:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print "Exception raised in %s" % inspect.trace()[-1][3]
                print entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], entry[7]

    def writerow(self, row, writer, queue, encoder, stream):
        try:
            writer.writerow([s.encode("utf-8") for s in row])
            # Fetch UTF-8 output from the queue ...
            data = queue.getvalue()
            data = data.decode("utf-8")
            # ... and reencode it into the target encoding
            data = encoder.encode(data)
            # write to the target stream
            stream.write(data)
            # empty queue
            queue.truncate(0)
        except Exception as E:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                print sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print "Exception raised in %s" % inspect.trace()[-1][3]
                print row

with open(self.dir+self.winunix+"scraped_headers.csv",'wb') as csvfile:
                csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL, delimiter=',')
                csvwriter.writerow(self.columns)
                csvwriter.writerows(2darray)

http://numpy-discussion.10968.n7.nabble.com/How-to-remove-any-row-or-column-of-a-numpy-matrix-whose-sum-is-3-td25574.html